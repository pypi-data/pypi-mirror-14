import codecs
from cStringIO import StringIO
from boto3.session import Session


class Ec2(object):
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name):
        session = Session(aws_access_key_id, aws_secret_access_key, region_name=region_name)
        self.__ec2 = session.resource('ec2')

    def start_instance(self, instance_id):
        instance = self.__ec2.Instance(instance_id)
        if instance.state['Name'] == 'running':
            return True
        instance.start()
        instance.wait_until_running()
        if instance.state['Name'] == 'running':
            return True
        return False

    def stop_instance(self, instance_id):
        instance = self.__ec2.Instance(instance_id)
        if instance.state['Name'] == 'stopped':
            return True
        instance.stop()
        instance.wait_until_stopped()
        if instance.state['Name'] == 'stopped':
            return True
        return False


class S3(object):
    def __init__(self, aws_access_key_id, aws_secret_access_key, region_name, retry_count=3):
        self.__retry_count = retry_count
        session = Session(aws_access_key_id, aws_secret_access_key, region_name=region_name)
        self.__s3 = session.resource('s3')

    def get_keys(self, bucket_name, prefix=''):
        bucket = self.__s3.Bucket(bucket_name)
        param = {
            'Prefix': prefix
        }
        for target_item in bucket.objects.filter(**param):
            yield target_item.key

    def download_ascii_file(self, bucket_name, key, local_file_path, encoding='utf-8', errors='ignore'):
        file_obj = codecs.open(local_file_path, 'w', encoding)
        for line in self.get_file_obj(bucket_name, key).getvalue().splitlines(True):
            file_obj.write(line.decode(encoding, errors))
        file_obj.close()

    def download_binary_file(self, bucket_name, key, local_file_path):
        self.__s3.meta.client.download_file(bucket_name, key, local_file_path)

    def get_file_obj(self, bucket_name, key):
        for _ in range(self.__retry_count):
            obj = self.__s3.Object(bucket_name, key)
            status_code = obj.get()['ResponseMetadata']['HTTPStatusCode']
            if status_code == 200:
                break
        else:
            raise Exception('can\'t get file from s3')
        return StringIO(obj.get()['Body'].read())

