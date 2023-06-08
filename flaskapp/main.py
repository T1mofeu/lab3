from PIL import Image, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import FileField, FloatField, SubmitField, StringField
from flask_wtf.recaptcha import RecaptchaField
from wtforms.validators import DataRequired

app = Flask(__name__, template_folder='D:/lab3')

app.config['SECRET_KEY'] = '6LccPn4mAAAAAKFVqnXNJ98ziiVkOfV5w8g6nxAb'
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LccPn4mAAAAAOZmNWkoWZ_JByUuOPwZVX9dIkBt'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LccPn4mAAAAAKFVqnXNJ98ziiVkOfV5w8g6nxAb'

def blend_images(image1, image2, alpha1, alpha2):

    return alpha1 * image1 + alpha2 * image2

def image_ret(image1, image2, blend_image, im_width):
    # отображение полученного изображения
    fig = plt.figure(figsize=(14, 7))

    # Первое изображение
    p1 = fig.add_subplot(2, 3, 1)
    p1.imshow(image1)

    # Второе изображение
    p2 = fig.add_subplot(2, 3, 2)
    p2.imshow(image2)

    p3 = fig.add_subplot(2, 3, 3)
    p3.imshow(blend_image)

    # График распределения цветов первого изображения
    imagea = image1 * 255
    imageb = image2 * 255
    imagec = blend_image * 255

    ax1 = fig.add_subplot(2, 3, 4)
    ax1.set(xlim=(0, im_width), ylim=(0, 255))
    ax1.plot(np.mean(imagea[:, :, 0], axis=0), 'r', label='Red')
    ax1.plot(np.mean(imagea[:, :, 1], axis=0), 'g', label='Green')
    ax1.plot(np.mean(imagea[:, :, 2], axis=0), 'b', label='Blue')
    ax1.set_xlabel('Column number')
    ax1.set_ylabel('Color channel value')
    ax1.set_title('Color channels of image1')
    ax1.legend()

    # График распределения цветов второго изображения
    ax2 = fig.add_subplot(2, 3, 5)
    ax2.set(xlim=(0, im_width), ylim=(0, 255))
    ax2.plot(np.mean(imageb[:, :, 0], axis=0), 'r', label='Red')
    ax2.plot(np.mean(imageb[:, :, 1], axis=0), 'g', label='Green')
    ax2.plot(np.mean(imageb[:, :, 2], axis=0), 'b', label='Blue')
    ax2.set_xlabel('Column number')
    ax2.set_ylabel('Color channel value')
    ax2.set_title('Color channels of image2')
    ax2.legend()

    ax3 = fig.add_subplot(2, 3, 6)
    ax3.set(xlim=(0, im_width), ylim=(0, 255))
    ax3.plot(np.mean(imagec[:, :, 0], axis=0), 'r', label='Red')
    ax3.plot(np.mean(imagec[:, :, 1], axis=0), 'g', label='Green')
    ax3.plot(np.mean(imagec[:, :, 2], axis=0), 'b', label='Blue')
    ax3.set_xlabel('Column number')
    ax3.set_ylabel('Color channel value')
    ax3.set_title('Color channels of image3')
    ax3.legend()

    plt.savefig('static/cc.jpg')
    # Вывод всего на экран

class MyForm(FlaskForm):
    image1 = FileField('Выберите изображение 1')
    image2 = FileField('Выберите изображение 2')
    x = FloatField('Выберите соотношение (от 0.0 до 1.0)')
    recaptcha = RecaptchaField()
    submit = SubmitField('Применить')

@app.route('/', methods=['GET', 'POST'])
def captcha():
    form = MyForm()
    if form.validate_on_submit():
        return render_template('one.html', form=form)
    return render_template('base.html', form=form)

@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        f1 = request.files['image1']
        f2 = request.files['image2']

        f1.save('aa.jpg')
        f2.save('bb.jpg')

        x = float(request.form['x'])
        file1 = Image.open('aa.jpg')
        file2 = Image.open('bb.jpg')

        max_width = max(file1.width, file2.width)
        max_height = max(file1.height, file2.height)

        file1 = file1.resize((max_width, max_height))

        file2 = file2.resize((max_width, max_height))

        im_width = max_width

        image1 = np.array(file1)/255.0
        image2 = np.array(file2)/255.0

        image_ret(image1, image2, blend_images(image1, image2, x, (1 - x)), im_width)
        return render_template("index.html")

# def one():
#     return render_template('one.html')
#
# def base():
#     return render_template("base.html")

if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)