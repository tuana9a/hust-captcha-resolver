# hust-captcha-resovler

nhận diện ảnh captcha ra text trong đó dùng thư viện [pbcquoc/vietocr](https://github.com/pbcquoc/vietocr)

## .env

`DEVICE=cpu` or `DEVICE=cuda:0`

## how to install

```bash
pip install --no-cache-dir -r requirements.txt
```

## how to run in docker

just test it

```bash
docker run --rm -it -p 5000:5000/tcp --env-file .env --memory 1g tuana9a/hust-captcha-resolver:latest
```

auto restart

```bash
docker run -d -p 5000:5000/tcp --env-file .env --memory 1g --restart unless-stopped tuana9a/hust-captcha-resolver:latest
```
