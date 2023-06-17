# hust-captcha-resovler

Nhận diện captcha Đại học Bách Khoa Hà Nội từ ảnh ra text

Mình sử dụng thư viện [pbcquoc/vietocr](https://github.com/pbcquoc/vietocr)

## set DEVICE in `.env` file

`.env` file

you use cpu `DEVICE=cpu`

you use gpu nvidia with cuda `DEVICE=cuda:0`

## weights

weights.pth [Google Drive](https://drive.google.com/file/d/1Yfz9JbA-I4cPuMXKNUQHZAmLu1rRVMCw/view?usp=sharing)

## how to install

```bash
pip install --no-cache-dir -r requirements.txt
```

## how to run

### docker

quick test

```bash
docker run --rm -it --env-file .env tuana9a/hust-captcha-resolver
```

long run with `docker-compose.yaml`

```bash
docker-compose up -d
```
