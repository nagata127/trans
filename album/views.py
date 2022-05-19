from django.forms import formset_factory
from django.shortcuts import redirect, render
from .models import *
from .forms import *
import django.views.generic as View

from PIL import Image
from googletrans import Translator

import sys
import pyocr
import pyocr.builders

def upload(request): # アップロード

    images = Document.objects.all() # モデルから画像取得

    # 言語切り替えのForm
    choice = LangChoiceForm()
    choice_form = LangChoiceFormSet

    # 言語初期値
    choice_lang = 'ja'
    choice_trans = 'en'
    choice = choice_form(initial = [
        {'select':choice_lang},
        {'select':choice_trans},
        ])

    if request.method == "POST": # POST時の処理
        #  アップロード処理
        form = ImageForm(request.POST, request.FILES)

        if form.is_valid(): # フォームに入力の際のエラー判定
            form.save()
        
        
        # プルダウン処理
        formset = choice_form(request.POST)

        if formset.is_valid():
            choice_lang = formset.cleaned_data[0]['select']
            choice_trans = formset.cleaned_data[1]['select']
            choice = choice_form(initial = [
                {'select':choice_lang},  # プルダウン選択言語の初期値変更
                {'select':choice_trans},
            ])
            
    
    else:
        form = ImageForm()

    # 画面を開いた時
    if request.method == 'GET':
        # モデルにある画像を削除
        images.delete()

    # 文字認識
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
                
        sys.exit(1)

    tool = tools[0]

    # 言語の選択・切り替え
    languages = {
        'ja':['jpn', '日本'],
        'en':['eng', '英語'],
        'fr':['fra', 'フランス'],
        'de':['deu', 'ドイツ'],
        'es':['spa', 'スペイン'],
        'he':['heb', 'ヘブライ']
        }

    try:
        if images: # モデルの中身がある時

            pic = images.order_by('-id')[0]
            img = Image.open(pic.photo.path)
                

            txt  = tool.image_to_string(
                img,
                lang  = languages[choice_lang][0],
                builder = pyocr.builders.TextBuilder(tesseract_layout = 6)
            )

            # 翻訳
            translator = Translator()
            
            #　文章を翻訳
            trans_txt = translator.translate(txt, src = choice_lang, dest = choice_trans).text
            # trans_en = translator.translate(txt, src = "ja", dest = "en").text

        else: # ないとき
            txt = ''
            trans_txt = ''

    except TypeError:
        txt = ''
        trans_txt = ''

    context = {
        'form':form,
        'images':images,
        'txt':txt,
        'trans_txt':trans_txt,
        'choice':choice,
        'lang':languages[choice_lang][1],
        'trans':languages[choice_trans][1],
        }
        
    return render(request, 'photo/index.html', context)
