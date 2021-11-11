# deploy config
scp -r resource/*.yaml resource/*.json ubuntu@vm1.aws.tuana9a.tech:/home/ubuntu/captcha2text/resource/
scp -r resource/*.yaml resource/*.json ubuntu@192.168.200.184:/home/ubuntu/captcha2text/resource/

# deploy weights
scp -r resource/*.pth ubuntu@vm1.aws.tuana9a.tech:/home/ubuntu/captcha2text/resource/
scp -r resource/*.pth ubuntu@192.168.200.184:/home/ubuntu/captcha2text/resource/

docker run -p 4000:80 --name captcha2text captcha2text
docker run -p 4000:80 --name captcha2text tuana9a/captcha2text

docker build --tag captcha2text .
docker build --tag captcha2text:1.0 .