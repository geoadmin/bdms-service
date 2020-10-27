# Changelog

## 1.0.2

### New features


 - **Borehole identifiers multilanguage**

    - Identifiers can be created and modified in each supported language.

 - **Text content management**

    - This feature is developed to handle multilanguage text (title and body) contents. Currently this feature is used to manage the text displayed in the login screen of web-bdms. (some default text is added in the databse)

 - **Handling database update process on upgrade**

    - The service will check the current version of the database and apply the required changes automatically if the 

## 1.0.1

### New features

 - **Feedback**: 
   
   Added new REST actions to handle user feedbacks.

 - **Terms of service**: 
   
   Added new REST actions to handle user agreements on *terms of service*.

 - **Login as viewer**: 
   
   Guest users can now access with the VIEW role.

 - **Attachments**: 
   
   You can now upload files attachments for each borehole on a AWS S3 Bucket.

 - **New configuration options**:
   
   - To configure the file repository some options have been added to configure the AWS S3 Bucket (file_repo, aws_bucket, aws_credentials)

   - feedback can be send throught and SMTP server to a configured email address.

 - **New REST API**:

   */api/v1/feedback*

   - ACTION=CREATE logged-in user can send a feedback message

   */api/v1/terms*

   - ACTION=ACCEPT logged-in user accept the current *terms of service*
   - ACTION=GET get the currently valid *terms of service*.

   */api/v1/terms/admin* (admin users only)

   - ACTION=GET Get the current draft *terms of service*.
   - ACTION=DRAFT Admins can update the current *terms of service* flagging it as *draft*.
   - ACTION=PUBLISH Promote the draft of *terms of service* to go public.

   */api/v1/borehole*

   - ACTION=LISTFILES list all files with less metadata linked to a given borehole

   */api/v1/borehole/edit*

   - ACTION=LISTFILES list all files metadata linked to a given borehole 
   
   */api/v1/borehole/edit/files*

   - ACTION=ATTACHFILE (multipart/form-data) and attach files to existing boreholes
   - ACTION=DETACHFILE unlink an uploaded file from a borehole
   - ACTION=PATCH update metadata of a file


 - **Database changes**:
   
   To handle the new attachments feature, two new tables were added to the
   schema bdms: **files** and **borehole_files**

 - **Simple Import with CSV**:
   
   As editor, importing new data using csv now handles more fields. In particular you can import easily a list of boreholes using this columns descriptors:

   - **location_east** (*numeric*): **mandatory**
   - **location_north** (*numeric*): **mandatory**
   - **public_name** (*text*): **mandatory**
   - location_z (*numeric*): *optional*
   - original_name (*text*): optional
   - project_name (*text*): optional
   - drilling_date (*text*): optional
   - total_depth (*numeric*): optional
   - top_bedrock (*numeric*): optional
   - remarks (*text*): optional

   Note: The column order can be exchanged.

### Backwards incompatible changes

 - **REST API Changes**:
   
   CSV importer API path has been changed from '/api/v1/borehole/upload' to
   '/api/v1/borehole/edit/import' and the POST-ed action param changed from
   'UPLOAD' to 'IMPORTCSV'

### Update from 1.0.0 to 1.0.0-RC1

Install boto3 in your python virtual env

```bash
source venv/bin/activate
```

Upgrade the postgresql schema by running this SQL script:

```bash
psql -U postgres -d bdms \
 -h localhost -p 9432 \
 -f assets/sql/1.0.0_to_1.0.1-RC1.sql
```
