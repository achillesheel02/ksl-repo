import os
import glob
import subprocess
import boto3

s3 = boto3.resource(
    service_name='s3',
    region_name='us-east-2',
    aws_access_key_id=os.environ["AWS_ACCESS_KEY"],
    aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"]
)

training_data_bucket = 'its-ability-raw-training-data'
csv_output_bucket = 'its-ability-csv-outputs'
annotated_videos_bucket = 'its-ability-annotated-videos'
location = 'us-east-2'
training_data = s3.Bucket(training_data_bucket).objects.all()

print('INFO: Checking if s3 buckets exist...')
if s3.Bucket(csv_output_bucket).creation_date:
    csv_outputs = s3.Bucket(csv_output_bucket).objects.all()
else:
    bucket = s3.create_bucket(Bucket=csv_output_bucket, CreateBucketConfiguration={'LocationConstraint':'us-east-2'},)
    csv_outputs = s3.Bucket(csv_output_bucket).objects.all()

if s3.Bucket(annotated_videos_bucket).creation_date:
    csv_outputs = s3.Bucket(annotated_videos_bucket).objects.all()
else:
    bucket = s3.create_bucket(Bucket=annotated_videos_bucket, CreateBucketConfiguration={'LocationConstraint':'us-east-2'},)
    csv_outputs = s3.Bucket(annotated_videos_bucket).objects.all()
print('INFO: Done.')
untrained_data = [item for item in training_data if item.key.split('.')[0].split('/')[1] not in csv_outputs]


training_videos = []

print('INFO: Files to convert: '+ str(len(untrained_data)))
print('INFO: Grabbing the data from the s3 bucket...')

for obj in untrained_data:
    label = obj.key.split('.')[0].split('/')[0]
    fileName = obj.key.split('.')[0].split('/')[1]
    input_url = "https://s3-%s.amazonaws.com/%s/%s" % (location, training_data_bucket, obj.key)
    training_videos.append([label, fileName, input_url])

print('INFO: Done grabbing tunconverted data.')

if __name__ == '__main__':
    path_to_mediapipe_binary = "bazel-bin/mediapipe/examples/desktop/multi_hand_tracking/multi_hand_tracking_tflite"
    graph = "mediapipe/graphs/hand_tracking/multi_hand_tracking_desktop.pbtxt"
    print('INFO: Generating csv files...')

    if len(training_videos) < 1:
        print("INFO: All files converted.")

    else:
        for index, item in enumerate(training_videos):
            print("File " +str(index+1) + " of " + str(len(training_videos)))
            input_video_path = item[2]
            label = item[0]
            fileName = item[1]
            output_video_path = fileName+'.mp4'
            output_csv_path = fileName+'.csv'
            cmd = [
                path_to_mediapipe_binary,
                "--calculator_graph_config_file=%s" % graph,
                "--input_side_packets=input_video_path=%s,output_video_path=%s" % (input_video_path, output_video_path),
                "--output_stream=multi_hand_landmarks",
                "--output_stream_file=%s" % output_csv_path
            ]
            print(subprocess.run(cmd))
            s3.meta.client.upload_file(output_video_path,annotated_videos_bucket,fileName+'.mp4')
            print('INFO: Uploaded annotated video')
            s3.meta.client.upload_file(output_csv_path, csv_output_bucket, fileName+'.csv')
            print('INFO: Uploaded CSV file')
            cmd = [
                "rm",
                output_csv_path,
                "&&",
                "rm",
                output_video_path
            ]
            print(subprocess.run(cmd))
        print('INFO: Done converting ' + str(len(training_videos)) + ' files.')
