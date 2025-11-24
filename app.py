from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from deep_translator import GoogleTranslator  # Вместо googletrans
import time  # Для time.time()
translator = GoogleTranslator(source='auto', target='ka')  # Глобально
app = Flask(__name__)

# Конфигурация (как раньше)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///incoming.db'
app.config['SQLALCHEMY_BINDS'] = {
    'news': 'sqlite:///news.db',
    'info': 'sqlite:///info.db',
    'history': 'sqlite:///history.db',
    'photo': 'sqlite:///photo.db',
    'translated': 'sqlite:///translated.db'
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs('uploads', exist_ok=True)

# Импорт db и моделей ПОСЛЕ конфигурации (важно!)
from Moduls import db, IncomingData, News, Info, History, Photo,TranslatedHistory,TranslatedNews,TranslatedInfo,TranslatedPhoto

# Привязываем db к app (теперь init_app вместо создания нового!)
db.init_app(app)

# Функция для проверки файлов (была пропущена)
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/add_data', methods=['POST'])
def add_data():
    # Проверяем текстовые поля
    title = request.form.get('title')
    intro = request.form.get('intro')
    text = request.form.get('text')
    key = request.form.get('key')

    if not all([title, intro, text, key]):
        return jsonify({'error': 'Все текстовые поля обязательны'}), 400

    # Дополнительные поля (опциональные)
    text2 = request.form.get('text2')
    text3 = request.form.get('text3')

    # Обработка файла
    image_path = None
    image_path1 = None
    image_path2 = None

    # Создаем и сохраняем запись в IncomingData (добавлено: логика сохранения)
    incoming_item = IncomingData(title=title, intro=intro, text=text, key=key, image_path=image_path, image_path1 = image_path1,image_path2 =image_path2, text2= text2,text3=text3)
    db.session.add(incoming_item)
    db.session.commit()

    return jsonify({'success': 'Данные добавлены успешно'}), 201

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/police')
def police():
    return render_template('police.html')

@app.route('/kar/police')
def police_kar():
    return render_template('police_kar.html')

@app.route('/news')                                 #1 news
def news(): #посты без сорта
    sor = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sor == 'date_asc':
        histor = History.query.order_by(History.datetime.desc()).all()
    else:
        histor = History.query.order_by(History.datetime.desc()).all()

    sorttt = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sorttt == 'date_asc':
        inform = Info.query.order_by(Info.datetime.desc()).all()
    else:
        inform = Info.query.order_by(Info.datetime.desc()).all()

    artic = News.query.order_by(News.datetime.desc()).all()
    sort = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sort == 'date_asc':
        articles = News.query.order_by(News.datetime.desc()).all()
    else:
        articles = News.query.order_by(News.datetime.desc()).all()
    return render_template('News.html', articles=articles,artic=artic,inform=inform,histor=histor)  # Исправлено: articles в шаблоне


@app.route('/news/<int:id>')                         #2 news
def news_detail(id):
    sor = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sor == 'date_asc':
        histor = History.query.order_by(History.datetime.desc()).all()
    else:
        histor = History.query.order_by(History.datetime.desc()).all()

    sorttt = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sorttt == 'date_asc':
        inform = Info.query.order_by(Info.datetime.desc()).all()
    else:
        inform = Info.query.order_by(Info.datetime.desc()).all()

    artic = News.query.get_or_404(id)
    sort = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sort == 'date_asc':
        articles = News.query.order_by(News.datetime.desc()).all()
    else:
        articles = News.query.order_by(News.datetime.desc()).all()
    return render_template('News1.html', articles=articles, artic=artic,inform=inform,histor=histor)

@app.route('/news/<int:id>/delete')                   #3 news
def delete_news(id):
    article = News.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/news')
    except Exception as e:
        db.session.rollback()
        return f"При удалении статьи произошла ошибка: {str(e)}"

@app.route('/info')                                 #1 info
def info():#посты без сорта
    artic = Info.query.order_by(Info.datetime.desc()).all()
    sort = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sort == 'date_asc':
        articles = Info.query.order_by(Info.datetime.desc()).all()
    else:
        articles = Info.query.order_by(Info.datetime.desc()).all()
    return render_template('about_geo.html', articles=articles, artic=artic)  # Исправлено: articles в шаблоне



@app.route('/info/<int:id>')                        #2 info
def info_detail(id):
    artic = Info.query.get_or_404(id)
    sort = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sort == 'date_asc':
        articles = Info.query.order_by(Info.datetime.desc()).all()
    else:
        articles = Info.query.order_by(Info.datetime.desc()).all()
    return render_template('about_geo1.html', articles=articles, artic=artic)

@app.route('/info/<int:id>/delete')                 #3 info
def delete_info(id):
    article = Info.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/info')
    except Exception as e:
        db.session.rollback()
        return f"При удалении статьи произошла ошибка: {str(e)}"


@app.route('/history')                                 #1 history
def history(): #посты без сорта
    artic = History.query.order_by(History.datetime.desc()).all()
    sort = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sort == 'date_asc':
        articles = History.query.order_by(History.datetime.desc()).all()
    else:
        articles = History.query.order_by(History.datetime.desc()).all()
    return render_template('history.html', articles=articles, artic=artic)  # Исправлено:


@app.route('/history/<int:id>')                                 #2 history
def history_detail(id):
    artic = History.query.get_or_404(id)  # Конкретная запись по ID

    sort = request.args.get('sort', 'id_desc')  # По умолчанию: ID desc (новые сначала)

    # Список всех записей с сортировкой только по ID
    if sort == 'id_asc':
        articles = History.query.order_by(History.id.desc()).all()
    else:  # id_desc или любой неверный
        articles = History.query.order_by(History.id.desc()).all()

    return render_template('history1.html', articles=articles, artic=artic)

@app.route('/history/<int:id>/delete')                                 #3 history
def delete_history(id):
    article = History.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/history')
    except Exception as e:
        db.session.rollback()
        return f"При удалении статьи произошла ошибка: {str(e)}"

@app.route('/photo')                                 #1 photo
def photo(): #посты без сорта (если только через айди)
    article = Photo.query.order_by().all()  # Добавлено: загрузка данных для consistency

    return render_template('photo.html', article=article)


@app.route('/photo/<int:id>')                                 #2 photo
def photo_detail(id):
    artic = Photo.query.get_or_404(id)  # Добавлено: детальный маршрут для photo
    return render_template('photo1.html', artic=artic)  # Предполагаем шаблон photo1.html

@app.route('/photo/<int:id>/delete')                                 #3 history
def delete_photo(id):
    article = Photo.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/photo')
    except Exception as e:
        db.session.rollback()
        return f"При удалении статьи произошла ошибка: {str(e)}"



@app.route('/kar/home')
def home_kar():
    return render_template('home_kar.html')


@app.route('/kar/news')                                 #1 news
def news_kar(): #посты без сорта
    sor = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sor == 'date_asc':
        histor = TranslatedHistory.query.order_by(TranslatedHistory.datetime.desc()).all()
    else:
        histor = TranslatedHistory.query.order_by(TranslatedHistory.datetime.desc()).all()

    sorttt = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sorttt == 'date_asc':
          inform = TranslatedInfo.query.order_by(TranslatedInfo.datetime.desc()).all()
    else:
          inform = TranslatedInfo.query.order_by(TranslatedInfo.datetime.desc()).all()


    artic = TranslatedNews.query.order_by(TranslatedNews.datetime.desc()).all()
    sort = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sort == 'date_asc':
        articles = TranslatedNews.query.order_by(TranslatedNews.datetime.desc()).all()
    else:
        articles = TranslatedNews.query.order_by(TranslatedNews.datetime.desc()).all()
    return render_template('News_kar.html', articles=articles,artic=artic,histor=histor,inform=inform)  # Исправлено: articles в шаблоне


@app.route('/kar/news/<int:id>')                         #2 news
def news_detail_kar(id):
    sor = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sor == 'date_asc':
        histor = TranslatedHistory.query.order_by(TranslatedHistory.datetime.desc()).all()
    else:
        histor = TranslatedHistory.query.order_by(TranslatedHistory.datetime.desc()).all()

    sorttt = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sorttt == 'date_asc':
        inform = TranslatedInfo.query.order_by(TranslatedInfo.datetime.desc()).all()
    else:
        inform = TranslatedInfo.query.order_by(TranslatedInfo.datetime.desc()).all()


    artic = TranslatedNews.query.get_or_404(id)
    sort = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sort == 'date_asc':
        articles = TranslatedNews.query.order_by(TranslatedNews.datetime.desc()).all()
    else:
        articles = TranslatedNews.query.order_by(TranslatedNews.datetime.desc()).all()
    return render_template('News1_kar.html', articles=articles, artic=artic,histor=histor,inform=inform)

@app.route('/kar/news/<int:id>/delete')                   #3 news
def delete_news_kar(id):
    article = TranslatedNews.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/kar/news')
    except Exception as e:
        db.session.rollback()
        return f"При удалении статьи произошла ошибка: {str(e)}"

@app.route('/kar/info')                                 #1 info
def info_kar():#посты без сорта
    artic = TranslatedInfo.query.order_by(TranslatedInfo.datetime.desc()).all()
    sort = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sort == 'date_asc':
        articles = TranslatedInfo.query.order_by(TranslatedInfo.datetime.desc()).all()
    else:
        articles = TranslatedInfo.query.order_by(TranslatedInfo.datetime.desc()).all()
    return render_template('about_geo_kar.html', articles=articles, artic=artic)  # Исправлено: articles в шаблоне



@app.route('/kar/info/<int:id>')                        #2 info
def info_detail_kar(id):
    artic = TranslatedInfo.query.get_or_404(id)
    sort = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sort == 'date_asc':
        articles = TranslatedInfo.query.order_by(TranslatedInfo.datetime.desc()).all()
    else:
        articles = TranslatedInfo.query.order_by(TranslatedInfo.datetime.desc()).all()
    return render_template('about_geo1_kar.html', articles=articles, artic=artic)

@app.route('/kar/info/<int:id>/delete')                 #3 info
def delete_info_kar(id):
    article = TranslatedInfo.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/kar/info')
    except Exception as e:
        db.session.rollback()
        return f"При удалении статьи произошла ошибка: {str(e)}"


@app.route('/kar/history')                                 #1 history
def history_kar(): #посты без сорта
    artic = TranslatedHistory.query.order_by(TranslatedHistory.datetime.desc()).all()
    sort = request.args.get('sort', 'date_desc')  # По умолчанию desc (новые сначала)
    if sort == 'date_asc':
        articles = TranslatedHistory.query.order_by(TranslatedHistory.datetime.desc()).all()
    else:
        articles = TranslatedHistory.query.order_by(TranslatedHistory.datetime.desc()).all()
    return render_template('history_kar.html', articles=articles, artic=artic)  # Исправлено:


@app.route('/kar/history/<int:id>')                                 #2 history
def history_detail_kar(id):
    artic = TranslatedHistory.query.get_or_404(id)  # Конкретная запись по ID

    sort = request.args.get('sort', 'id_desc')  # По умолчанию: ID desc (новые сначала)

    # Список всех записей с сортировкой только по ID
    if sort == 'id_asc':
        articles = TranslatedHistory.query.order_by(TranslatedHistory.id.desc()).all()
    else:  # id_desc или любой неверный
        articles = TranslatedHistory.query.order_by(TranslatedHistory.id.desc()).all()

    return render_template('history1_kar.html', articles=articles, artic=artic)

@app.route('/kar/history/<int:id>/delete')                                 #3 history
def delete_history_kar(id):
    article = TranslatedHistory.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/kar/history')
    except Exception as e:
        db.session.rollback()
        return f"При удалении статьи произошла ошибка: {str(e)}"

@app.route('/kar/photo')                                 #1 photo
def photo_kar(): #посты без сорта (если только через айди)
    article = TranslatedPhoto.query.order_by().all()  # Добавлено: загрузка данных для consistency
    return render_template('photo_kar.html', article=article)


@app.route('/kar/photo/<int:id>')                                 #2 photo
def photo_detail_kar(id):
    artic = TranslatedPhoto.query.get_or_404(id)  # Добавлено: детальный маршрут для photo
    return render_template('photo1.html', artic=artic)  # Предполагаем шаблон photo1.html

@app.route('/kar/photo/<int:id>/delete')                                 #3 history
def delete_photo_kar(id):
    article = TranslatedPhoto.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/kar/photo')
    except Exception as e:
        db.session.rollback()
        return f"При удалении статьи произошла ошибка: {str(e)}"


@app.route('/IncomingData')                                #1 IncomingData
def posts():
    articles = IncomingData.query.order_by(IncomingData.datetime.desc()).all()  # Предполагаем поле datetime в модели
    return render_template('posts.html', articles=articles)

@app.route('/IncomingData/<int:id>')                                 #2 IncomingData
def post_detail(id):
    article = IncomingData.query.get_or_404(id)
    return render_template('posts_detal.html', article=article)

@app.route('/IncomingData/<int:id>/delete')                                #3 IncomingData
def delete_post(id):
    article = IncomingData.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except Exception as e:
        db.session.rollback()
        return f"При удалении статьи произошла ошибка: {str(e)}"


from deep_translator import GoogleTranslator

@app.route('/posts_adm', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        try:
            # --- Извлекаем данные из формы ---
            key = request.form.get('key')
            title = request.form.get('title')
            intro = request.form.get('intro')
            text = request.form.get('text', '')
            text2 = request.form.get('text2', '')
            text3 = request.form.get('text3', '')
            image_path = request.form.get('image_path')
            image_path1 = request.form.get('image_path1')
            image_path2 = request.form.get('image_path2')

            # --- Инициализация переводчика (целевая язык, например, 'en' для английского; подставьте ваш) ---
            translator = GoogleTranslator(source='auto', target='ka')  # 'auto' для автоматического определения исходного языка

            # --- Переведённые поля ---
            translated_title = translator.translate(title) if title else ''
            translated_intro = translator.translate(intro) if intro else ''
            translated_text = translator.translate(text) if text else ''
            translated_text2 = translator.translate(text2) if text2 else ''
            translated_text3 = translator.translate(text3) if text3 else ''

            # --- Базовая валидация ---
            if key not in ['news', 'info', 'history', 'photo']:
                return render_template('posts_create.html', error='Неверный key. Допустимые: news, info, history, photo')
            if key == 'photo' and not image_path:
                return render_template('posts_create.html', error='Для photo обязательна ссылка на изображение!')
            if not title or not intro:
                return render_template('posts_create.html', error='Обязательные поля: title и intro')

            # --- Выбор классов (убираем дублирование) ---
            if key == 'news':
                ItemClass = News
                TransClass = TranslatedNews
            elif key == 'info':
                ItemClass = Info
                TransClass = TranslatedInfo
            elif key == 'history':
                ItemClass = History
                TransClass = TranslatedHistory
            else:  # photo
                ItemClass = Photo
                TransClass = TranslatedPhoto

            # --- Создаём оригинал ---
            if key != 'photo':
                item = ItemClass(
                    title=title, intro=intro, text=text,
                    image_path=image_path, image_path1=image_path1, image_path2=image_path2,
                    text2=text2, text3=text3
                )
            else:
                item = ItemClass(
                    title=title, intro=intro,
                    image_path=image_path, image_path1=image_path1, image_path2=image_path2
                )
            db.session.add(item)
            db.session.flush()
            original_id = item.id

            # --- Перевод оригинала ---
            if key != 'photo':
                trans_item = TransClass(
                    title=translated_title, intro=translated_intro, text=translated_text,
                    text2=translated_text2, text3=translated_text3,
                    image_path=image_path, image_path1=image_path1, image_path2=image_path2,
                    original_id=original_id
                )
            else:
                trans_item = TransClass(
                    title=translated_title, intro=translated_intro,
                    image_path=image_path, image_path1=image_path1, image_path2=image_path2,
                    original_id=original_id
                )
            db.session.add(trans_item)

            # --- Если есть фото и это НЕ ключ "photo" — создаём отдельную запись Photo ---
            if key != 'photo' and image_path:
                photo = Photo(
                    title=title, intro=intro,
                    image_path=image_path, image_path1=image_path1, image_path2=image_path2
                )
                db.session.add(photo)
                db.session.flush()
                photo_id = photo.id

                trans_photo = TranslatedPhoto(
                    title=translated_title, intro=translated_intro,
                    image_path=image_path, image_path1=image_path1, image_path2=image_path2,
                    original_id=photo_id
                )
                db.session.add(trans_photo)

            # --- ОДИН commit для всей транзакции ---
            db.session.commit()

            return redirect(url_for('home'))

        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Ошибка создания поста: {str(e)}")
            return render_template('posts_create.html', error=f'Ошибка при сохранении: {str(e)}')

    # GET-запрос
    return render_template('posts_create.html')






if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Теперь без ошибки!
    app.run(host='0.0.0.0', port=5000, debug=True)