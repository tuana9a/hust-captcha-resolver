# hust-captcha-resovler

Nhận diện captcha Đại học Bách Khoa Hà Nội từ ảnh ra text. Project này mình nhờ thằng bạn mình train model sử dụng thư viện [pbcquoc/vietocr](https://github.com/pbcquoc/vietocr) để làm image to text.

Thằng bạn mình tên Chiến giờ nó đang PhD student bên đại học Oregon của mẽo. Nó giỏi vl.

- Tỉ lệ nhận diện đúng khoảng 80%, có thể chạy trên CPU
- Mình có đang host predictor này bằng một server 1 core, 1 GB ram thì thời gian predict một ảnh khoảng 0.5s (chậm lâu tùy lúc)

Nếu các bạn không muốn tự deploy có thể dùng sẵn URL này https://hcr.tuana9a.com

```http
POST https://hcr.tuana9a.com
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="file"; filename="23704_1632185498725.png"
Content-Type: image/png

< ./samples/23704_1632185498725.png
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

## weights

weights.pth https://public.tuana9a.com/hust-captcha-resolver/weights-2021.04.05.pth

## how to install

mình mới test ở `python3.8`, các phiên bản python khác cần thời gian để test thêm

```bash
pip install --no-cache-dir -r requirements.txt
```

ngoài ra trong lúc cài requirements có thể cần cài thêm các apt package sau

```bash
sudo apt install libjpeg-dev
```

## how to run

### env variables

examples

`PORT`=`8080`

`BIND`=`127.0.0.1`

`DEVICE`=`cpu`

or `DEVICE`=`cuda:0`

`UPLOAD_RATE_LIMIT`=`5/5second`

### docker

quick test

```bash
docker run --rm -p 8080:8080 -it --env-file .env tuana9a/hust-captcha-resolver
```

### `docker-compose.yaml`

```yaml
version: "3"

services:
  hcr:
    image: tuana9a/hcr
    container_name: hcr
    build: .
    ports:
      - 8080:8080
    env_file: .env
    restart: unless-stopped
```

```bash
docker-compose up -d
```
