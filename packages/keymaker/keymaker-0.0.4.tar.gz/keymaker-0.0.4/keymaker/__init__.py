"""
TODO:
- hostkey propagation via cloud-init hostkey upload / ssh client hostkey verification hook
- group propagation (incl. sudoers)
- store all keys in key pair objects; only metadata in S3
- efs integration
"""

from __future__ import absolute_import, division, print_function, unicode_literals

from io import open

import os, sys, json, time, logging, subprocess, pwd

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logging.getLogger("botocore.vendored.requests").setLevel(logging.DEBUG)

# TODO: integration with watchtower

#cloudtrail = boto3.client("cloudtrail")
#iam=boto3.resource("iam")
#s3=boto3.resource("s3")
#sqs=boto3.resource("sqs")
#sqs_client=boto3.client("sqs")

#response = client.create_trail(Name=__name__, S3BucketName=__name__)

"""

> keymaker
Using AWS key: <KEY ID>
Account ID: <ID>
Checking if key has admin privileges... GREEN(OK)
Your account is not configured for use with Keymaker. Exiting.
Your account is not configured for use with Keymaker. Configure now? [y/n] Please answer yes or no.
Configuring account.
Creating S3 bucket "..."... GREEN(OK)
Setting permissions... GREEN(OK)
Done! Next steps:

* Install Keymaker on your hosts with BOLD(keymaker install).
* Upload user SSH credentials with BOLD(keymaker upload).

> keymaker install
> keymaker upload

supervisor run
- ensure bucket/perms

See http://docs.aws.amazon.com/AmazonS3/latest/dev/example-policies-s3.html
{
   "Version":"2012-10-17",
   "Statement":[
      {
         "Effect":"Allow",
         "Action":[
            "s3:PutObject",
            "s3:GetObject",
            "s3:GetObjectVersion",
            "s3:DeleteObject",
            "s3:DeleteObjectVersion"
         ],
         "Resource":"arn:aws:s3:::examplebucket/${aws:username}/*"
      }
   ]
}

- ensure specified or current user has corresponding IAM user
- set bucket policies

client run
- "keymaker upload [--user u] [--public-key id.pub]"
- ensure bucket/perms
- ensure specified or current user has corresponding IAM user
- upload specified or current user pubkey
- set uid (Q: how to make this transactional?)
- Q: How to sync groups?

daemon run
- check bucket/perms or quit
- list all IAM users who have network access to this instance and are in the ssh group
- for each IAM user:
  - create if necessary
  - copy pubkeys to authorized
  - for any pubkey in authorized not in IAM: disable it
  - if userdata contains deny password access option, deny password access?
- for each local user with no IAM user:
  - if in range, issue warning
  - if userdata contains force option, disable user

- write cloudtrail log whenever adding or deleting user/group
- installing daemon via userdata/cloud-init
"""

from collections import namedtuple

class ARN(namedtuple("ARN", "partition service region account resource")):
    def __str__(self):
        return ":".join(["arn"] + list(self))

ARN.__new__.__defaults__ = ("aws", "", "", "", "")

def parse_arn(arn):
    return ARN(*arn.split(":", 5)[1:])

def get_bucket():
    account_id = parse_arn(iam.CurrentUser().arn).account
    bucket = s3.Bucket("{name}-{account}".format(name=__name__, account=account_id))
    bucket.create()
    bucket.wait_until_exists()

    response = cloudtrail.create_trail(Name=__name__, S3BucketName=bucket.name)

    return bucket

def get_group(name="ssh"):
    ssh_group = iam.Group(name)
    try:
        ssh_group.create()
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") != "EntityAlreadyExists":
            raise
    return ssh_group

def build_policy_doc(bucket, prefix="/*", perms="r"):
    actions = []
    if "r" in perms:
        actions.extend(["s3:ListBucket", "s3:GetObject"])
    if "w" in perms:
        actions.extend(["s3:PutObject", "s3:DeleteObject"])
    doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": actions,
                "Resource": [str(ARN(service="s3", resource=bucket.name)),
                             str(ARN(service="s3", resource=bucket.name + prefix))]
            }
        ]
    }
    return json.dumps(doc)

def set_permissions(bucket):
    ssh_admin_group = get_group(name="ssh_admin")
    ssh_admin_group.create_policy(PolicyName="keymaker-ssh-admin",
                                  PolicyDocument=build_policy_doc(bucket, perms="rw"))
    ssh_admin_group.add_user(UserName=iam.CurrentUser().user_name)

    ssh_group = get_group()
    ssh_group.create_policy(PolicyName="keymaker-ssh-group",
                            PolicyDocument=build_policy_doc(bucket, perms="r"))
    for user in iam.users.all():
        ssh_group.add_user(UserName=user.name)
        user.create_policy(PolicyName="keymaker-ssh-user",
                           PolicyDocument=build_policy_doc(bucket, perms="w", prefix="/users/" + user.name))

    # TODO: delete all other policies concerning this bucket - must be done by enumerating all policies for all users/groups?

"""
def set_notifications(bucket):
    queue = sqs_client.create_queue(QueueName="keymaker"

    config = {
        'QueueConfiguration': {
            'Id': STRING,
        'Event': STRING,
        'Events': [
            STRING,
            ...
        ],
        'Queue': STRING
    },
    'CloudFunctionConfiguration': {
        'Id': STRING,
        'Event': STRING,
        'Events': [
            STRING,
            ...
        ],
        'CloudFunction': STRING,
        'InvocationRole': STRING
    }
}
    bn = bucket.Notification().put(config, md5)
"""

def upload_public_key(bucket, user, key_name, key_body):
    return bucket.put_object(Key="/users/{user}/{key}".format(user=user, key=key_name),
                             Body=key_body)

def download_public_key(bucket, user, key_name, key_body):
    return bucket.Object("/users/{user}/{key}".format(user=user, key=key_name)).get()

"""
from datetime import datetime
from dateutil.tz import tzutc
def watch(bucket, interval=5):
    last_checked_at = datetime.fromtimestamp(0, tzutc())
    while True:
        t = datetime.now(tzutc())
        print("Checking", bucket)
        for obj in bucket.objects.filter(Prefix="/"):
            if obj.last_modified > last_checked_at:
                print("Processing", obj)

        last_checked_at = t
        time.sleep(interval)
"""

def configure(args):
    print("Will configure", args)

def get_authorized_keys(args):
    iam = boto3.client("iam")
    for key_desc in iam.list_ssh_public_keys(UserName=args.user)["SSHPublicKeys"]:
        key = iam.get_ssh_public_key(UserName=args.user, SSHPublicKeyId=key_desc["SSHPublicKeyId"], Encoding="SSH")
        if key["SSHPublicKey"]["Status"] == "Active":
            print(key["SSHPublicKey"]["SSHPublicKeyBody"])

def install(args):
    user = args.user or "keymaker"
    try:
        pwd.getpwnam(user)
    except KeyError:
        subprocess.check_call(["useradd", user,
                               "--comment", "Keymaker SSH key daemon",
                               "--shell", "/usr/sbin/nologin"])

    authorized_keys_script_path = "/usr/sbin/keymaker-get-public-keys"
    with open(authorized_keys_script_path, "w") as fh:
        print("#!/bin/bash -e", file=fh)
        print('keymaker get_authorized_keys "$@"', file=fh)
    subprocess.check_call(["chown", "root", authorized_keys_script_path])
    subprocess.check_call(["chmod", "go-w", authorized_keys_script_path])

    with open("/etc/ssh/sshd_config") as fh:
        sshd_config = fh.readlines()
    config_lines = [
        "AuthorizedKeysCommand " + authorized_keys_script_path,
        "AuthorizedKeysCommandUser " + user,
        "ChallengeResponseAuthentication yes",
        "AuthenticationMethods publickey keyboard-interactive:pam,publickey"
    ]
    with open("/etc/ssh/sshd_config", "a") as fh:
        for line in config_lines:
            if line not in sshd_config:
                print(line, file=fh)

    # TODO: print explanation if errors occur
    subprocess.check_call(["sshd", "-t"])

    pam_config_line = "auth requisite pam_exec.so stdout /usr/local/bin/keymaker-create-account-for-iam-user"
    with open("/etc/pam.d/sshd") as fh:
        pam_config_lines = fh.readlines()
    pam_config_lines.insert(1, pam_config_line)
    with open("/etc/pam.d/sshd", "w") as fh:
        for line in pam_config_lines:
            print(line, file=fh)

def err_exit(msg, code=3):
    print(msg, file=sys.stderr)
    exit(code)

def load_ssh_public_key(filename):
    with open(filename) as fh:
        key = fh.read()
        if "PRIVATE KEY" in key:
            logger.info("Extracting public key from private key {}".format(filename))
            key = subprocess.check_output(["ssh-keygen", "-y", "-f", filename]).decode()
    return key

def select_ssh_public_key(identity=None):
    if identity:
        if not os.path.exists(identity):
            err_exit("Path {} does not exist".format(identity))
        return load_ssh_public_key(identity)
    else:
        try:
            keys = subprocess.check_output(["ssh-add", "-L"]).decode("utf-8").splitlines()
            if len(keys) > 1:
                exit('Multiple keys reported by ssh-add. Please specify a key filename with --identity or unload keys with "ssh-add -D", then load the one you want with "ssh-add ~/.ssh/id_rsa" or similar.')
            return keys[0]
        except subprocess.CalledProcessError:
            default_path = os.path.expanduser("~/.ssh/id_rsa.pub")
            if os.path.exists(default_path):
                logger.warning('Using {} as your SSH key. If this is not what you want, specify one with --identity or load it with ssh-add'.format(default_path))
                return load_ssh_public_key(default_path)
            exit('No keys reported by ssh-add, and no key found in default path. Please run ssh-keygen to generate a new key, or load the one you want with "ssh-add ~/.ssh/id_rsa" or similar.')

def upload(args):
    ssh_public_key = select_ssh_public_key(args.identity)
    iam = boto3.resource("iam")
    user = iam.CurrentUser().user
    from botocore.exceptions import ClientError
    try:
        user.meta.client.upload_ssh_public_key(UserName=user.name, SSHPublicKeyBody=ssh_public_key)
    except ClientError as e:
        if e.response.get("Error", {}).get("Code") == "LimitExceeded":
            logger.error('The current IAM user has filled their public SSH key quota. Delete keys with "aws iam list-ssh-public-keys; aws iam delete-ssh-public-key --user-name USER --ssh-public-key-id KEY_ID".')
        raise


    #    import paramiko
#    for key in paramiko.agent.Agent().get_keys():
#        print(key.get_name() + " " + key.get_base64(), dir(key), key.__dict__)
    #print("Select an SSH key pair to use when connecting to EC2 instances. The public key will be saved to your IAM user account. The private key will remain on this computer.")
    #for identity in subprocess.check
    # TODO: enum regions
#    ssh_key = new_ssh_key()
    #user.meta.client.upload_ssh_public_key(UserName=user.name, SSHPublicKeyBody=public_key(ssh_key))
#    ssh_key.write_private_key_file(get_key_path("keymaker"))
#    for key in user.meta.client.list_ssh_public_keys(UserName=user.name)["SSHPublicKeys"]:
#        print(user, key, user.meta.client.get_ssh_public_key(UserName=user.name, SSHPublicKeyId=key["SSHPublicKeyId"], Encoding="SSH")["SSHPublicKey"]["SSHPublicKeyBody"])
