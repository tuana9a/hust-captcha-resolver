# hust-captcha-resovler

Nhận diện captcha Đại học Bách Khoa Hà Nội từ ảnh ra text

Mình sử dụng thư viện [pbcquoc/vietocr](https://github.com/pbcquoc/vietocr)

## set DEVICE in `.env` file

`.env` file

you use cpu `DEVICE=cpu`

you use gpu nvidia with cuda `DEVICE=cuda:0`

## weights

weights.pth [https://public.tuana9a.com/hust-captcha-resolver/weights-2021.04.05.pth](https://public.tuana9a.com/hust-captcha-resolver/weights-2021.04.05.pth)

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
