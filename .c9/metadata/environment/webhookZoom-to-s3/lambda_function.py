{"filter":false,"title":"lambda_function.py","tooltip":"/webhookZoom-to-s3/lambda_function.py","undoManager":{"mark":8,"position":8,"stack":[[{"start":{"row":2,"column":0},"end":{"row":2,"column":22},"action":"remove","lines":["import requests as res"],"id":2}],[{"start":{"row":8,"column":4},"end":{"row":8,"column":6},"action":"remove","lines":["# "],"id":3},{"start":{"row":9,"column":4},"end":{"row":9,"column":6},"action":"remove","lines":["# "]},{"start":{"row":10,"column":4},"end":{"row":10,"column":6},"action":"remove","lines":["# "]},{"start":{"row":11,"column":4},"end":{"row":11,"column":6},"action":"remove","lines":["# "]},{"start":{"row":12,"column":16},"end":{"row":12,"column":17},"action":"remove","lines":["#"]},{"start":{"row":13,"column":16},"end":{"row":13,"column":17},"action":"remove","lines":["#"]}],[{"start":{"row":11,"column":16},"end":{"row":11,"column":20},"action":"remove","lines":["pass"],"id":4},{"start":{"row":11,"column":12},"end":{"row":11,"column":16},"action":"remove","lines":["    "]},{"start":{"row":11,"column":8},"end":{"row":11,"column":12},"action":"remove","lines":["    "]},{"start":{"row":11,"column":4},"end":{"row":11,"column":8},"action":"remove","lines":["    "]},{"start":{"row":11,"column":0},"end":{"row":11,"column":4},"action":"remove","lines":["    "]},{"start":{"row":10,"column":77},"end":{"row":11,"column":0},"action":"remove","lines":["",""]}],[{"start":{"row":2,"column":0},"end":{"row":2,"column":1},"action":"insert","lines":["i"],"id":5},{"start":{"row":2,"column":1},"end":{"row":2,"column":2},"action":"insert","lines":["m"]},{"start":{"row":2,"column":2},"end":{"row":2,"column":3},"action":"insert","lines":["o"]}],[{"start":{"row":2,"column":2},"end":{"row":2,"column":3},"action":"remove","lines":["o"],"id":6}],[{"start":{"row":2,"column":2},"end":{"row":2,"column":3},"action":"insert","lines":["p"],"id":7},{"start":{"row":2,"column":3},"end":{"row":2,"column":4},"action":"insert","lines":["o"]},{"start":{"row":2,"column":4},"end":{"row":2,"column":5},"action":"insert","lines":["r"]},{"start":{"row":2,"column":5},"end":{"row":2,"column":6},"action":"insert","lines":["t"]}],[{"start":{"row":2,"column":6},"end":{"row":2,"column":7},"action":"insert","lines":[" "],"id":8},{"start":{"row":2,"column":7},"end":{"row":2,"column":8},"action":"insert","lines":["r"]},{"start":{"row":2,"column":8},"end":{"row":2,"column":9},"action":"insert","lines":["e"]},{"start":{"row":2,"column":9},"end":{"row":2,"column":10},"action":"insert","lines":["q"]},{"start":{"row":2,"column":10},"end":{"row":2,"column":11},"action":"insert","lines":["u"]},{"start":{"row":2,"column":11},"end":{"row":2,"column":12},"action":"insert","lines":["e"]},{"start":{"row":2,"column":12},"end":{"row":2,"column":13},"action":"insert","lines":["s"]},{"start":{"row":2,"column":13},"end":{"row":2,"column":14},"action":"insert","lines":["t"]}],[{"start":{"row":2,"column":14},"end":{"row":2,"column":15},"action":"insert","lines":["s"],"id":9}],[{"start":{"row":3,"column":0},"end":{"row":7,"column":22},"action":"remove","lines":["","def lambda_handler(event, context):","    ","    directories = os.popen(\"ls /opt/\").read().split(\"\\n\")","    print(directories)"],"id":10,"ignore":true},{"start":{"row":3,"column":0},"end":{"row":24,"column":4},"action":"insert","lines":["import logging","import boto3","import uuid","from botocore.exceptions import ClientError","","","def lambda_handler(event, context):","    #print(event)","    evento = json.loads(event[\"body\"])","    ","    #Zoom meta data from the webhook","    download_token = evento[\"download_token\"]","    account_id = evento[\"payload\"][\"account_id\"]","    host_id = evento[\"payload\"][\"object\"][\"host_id\"]","    topic = evento[\"payload\"][\"object\"][\"topic\"].replace(\" \",\"\")","    base = \"{}/{}/{}/\".format(account_id,host_id,topic)","    ","    if \"bucket\" in os.environ :","        s3bucket = os.getenv(\"bucket\")","    else :","        s3bucket = \"notasdofelip\"","    "]},{"start":{"row":25,"column":22},"end":{"row":25,"column":23},"action":"insert","lines":["o"]},{"start":{"row":26,"column":8},"end":{"row":36,"column":0},"action":"remove","lines":["if \"recording_type\" in media :","            if media[\"recording_type\"] == \"shared_screen_with_speaker_view\" :","                response = requests.get(media[\"download_url\"])","                print (response)","","    ","    return {","        'statusCode': 200,","        'body': json.dumps('Hello from Lambda!')","    }",""]},{"start":{"row":26,"column":8},"end":{"row":72,"column":15},"action":"insert","lines":["print(media[\"file_type\"])","        meeting_id = media[\"meeting_id\"]","        ","        tmp = str(uuid.uuid4())","        ","        name = base + meeting_id + \".\" + media[\"file_type\"]","        ","        print(\"Token : \"+ download_token)","        print(\"Url:\" + media[\"download_url\"] )","        response = requests.get(media[\"download_url\"] + \"?access_token=\" + download_token )","        with open(\"/tmp/\"+tmp, 'wb') as fd:","            for chunk in response.iter_content(chunk_size=128):","                fd.write(chunk)","        print(\"wrote file {}\".format(name))","        fd.close()","        if upload_file(\"/tmp/\"+tmp, s3bucket,name) :","            print(\"Uploaded file {} to {}\".format(name,s3bucket))","        else :","            print(\"error uploading file to s\")","    ","    return {","        'statusCode': 200,","        'body': json.dumps('{} uploaded to bucket {}'.format(name,s3bucket))","    }","","def upload_file(file_name, bucket, object_name=None):","    \"\"\"Upload a file to an S3 bucket","","    :param file_name: File to upload","    :param bucket: Bucket to upload to","    :param object_name: S3 object name. If not specified then file_name is used","    :return: True if file was uploaded, else False","    \"\"\"","","    # If S3 object_name was not specified, use file_name","    if object_name is None:","        object_name = file_name","","    # Upload the file","    s3_client = boto3.client('s3')","    try:","        response = s3_client.upload_file(file_name, bucket, object_name)","        print(\"uploaded file: \"+ file_name)","    except ClientError as e:","        logging.error(e)","        return False","    return True"]}]]},"ace":{"folds":[],"scrolltop":0,"scrollleft":0,"selection":{"start":{"row":9,"column":17},"end":{"row":9,"column":17},"isBackwards":false},"options":{"guessTabSize":true,"useWrapMode":false,"wrapToView":true},"firstLineState":0},"timestamp":1587918930269,"hash":"112400a304d213a3c4974673467a44a8e6e6caef"}