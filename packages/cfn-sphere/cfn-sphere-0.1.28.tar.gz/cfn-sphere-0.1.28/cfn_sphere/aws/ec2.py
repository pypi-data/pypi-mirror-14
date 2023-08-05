from boto import ec2
from boto.exception import BotoServerError
from cfn_sphere.exceptions import CfnSphereException, CfnSphereBotoError
from cfn_sphere.util import with_boto_retry


class Ec2Api(object):
    def __init__(self, region="eu-west-1"):
        self.conn = ec2.connect_to_region(region)

    @with_boto_retry()
    def get_taupage_images(self):
        filters = {'name': ['Taupage-AMI-*'],
                   'is-public': ['false'],
                   'state': ['available'],
                   'root-device-type': ['ebs']
                   }
        try:
            response = self.conn.get_all_images(executable_by=["self"], filters=filters)
        except BotoServerError as e:
            raise CfnSphereBotoError(e)

        if not response:
            raise CfnSphereException("Could not find any private and available Taupage AMI")

        return response

    def get_latest_taupage_image_id(self):
        images = {image.creationDate: image.id for image in self.get_taupage_images()}

        creation_dates = list(images.keys())
        creation_dates.sort(reverse=True)
        return images[creation_dates[0]]
