# AWS - Boto3

  * AWS SDK for Python (Boto3) to create, configure, and manage AWS services, such as Amazon Elastic Compute Cloud (Amazon EC2) and Amazon Simple Storage Service (Amazon S3).
  * The SDK provides an object-oriented API as well as low-level access to AWS services.

## STS: 
A low-level client representing AWS Security Token Service (STS)
  * Security Token Service (STS) enables us to request temporary, limited-privilege credentials for users.
  * Temporary security credentials:
      * Temporary security credentials are short-term, as the name implies. They can be configured to last for anywhere from a few minutes to several hours. After the credentials expire, AWS no longer recognizes them or allows any kind of access from API requests made with them
  * assume_role
      * Returns a set of temporary security credentials that you can use to access Amazon Web Services resources. These temporary credentials consist of an access key ID, a secret access key, and a security token.
