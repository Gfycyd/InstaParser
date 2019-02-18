import re
import time
import urllib.error
import threading
import requests

from django.shortcuts import render
# Create your views here.\
import excel_writer
import my_work.insta_parser
from .forms import QueryForm, QueryCount
from config import table_excel

def waiter(request):
    form = QueryForm()
    count = QueryCount()
    time.sleep(5)
    try:
        info = "Ваша таблица очищена сейчас, вы можете это проверить"
        excel_writer.delete(table_excel)
        args = {'info': info, 'form':form, 'table': table_excel, 'count':count}
        return render(request, 'main.html', args)
    except:
        waiter(request)
def get_req(request):
    for i in request.GET.keys():
        count = QueryCount()
        if i == 'deleter':
            try:
           # excel_writer.delete()
                form = QueryForm()

                excel_writer.delete(table_excel)

                info = "Ваша таблица очищена, можно начать заполнение"
                args = {'info': info, 'form': form, 'html': table_excel,'count':count}
                return render(request, 'main.html', args)
            except:
                waiter(request)
        else:
            form = QueryForm()
            return render(request, 'main.html', {'form': form, 'html': table_excel, 'count': count})
    form = QueryForm()
    count = QueryCount()
    return render(request, 'main.html', {'form': form, 'html':table_excel, 'count': count })
def main(request):
        return catch(request)

def catch(request):
        try:
            if request.method == 'POST':
                form = QueryForm(request.POST)
                if form.is_valid():
                    text = form.cleaned_data['q']
                    if text[0] == "#" and re.match(re.compile(r'#[a-zA-Z0-9а-яА-Я_]+'), text) and not ' ' in text:
                        type = "hashtag"
                        number = QueryCount(request.POST)
                        if number.is_valid():
                            ups = number.cleaned_data['count']
                        else:
                            ups = -1

                        my_work.insta_parser.search(type, text[1:len(text)],table_excel, ups)
                        args = {'type':str(type)+" : "+str(text),'html':table_excel,'exist':'Получить результаты запроса'}
                        return render(request, "answer.html", args)

                    elif text[0] == "@" and re.match(re.compile(r'@[a-z_.0-9]+'), text) and not ' ' in text:
                        type = "login"
                        number = QueryCount(request.POST)
                        if number.is_valid():
                            ups = number.cleaned_data['count']
                        else:
                            ups = 0
                        t = threading.Thread(target=my_work.insta_parser.search(type, text[1:len(text)], table_excel, ups))
                        t.setDaemon(True)
                        t.start()
                        return render(request, "answer.html", {'type':str(type)+" : "+str(text),'html':table_excel, 'exist':'Получить результаты запроса'})
                    else:
                    # form = QueryForm()
                        info1 = "Поиск по хештегу: #ваштекст  (без пробелов, не менее 2 символов) "
                        info2 = "Поиск по логину: @нужныйлогин (без пробелов, не менее 2 символов)"
                        type = ""
                        info = "Ошибочно введены данные"
                        count = QueryCount()
                        args = {'form':form, 'info': info, 'info1': info1,"info2": info2, 'type': type, 'count':count}
                        return render(request, "main.html", args)

        except urllib.error.HTTPError:
            info = "Нет результатов по введенному запросу"
            form = QueryForm(request.POST)
            if form.is_valid():
                text = form.cleaned_data['q']

                if text[0] == "#": type = "hashtag"
                elif text[0] == "@": type = "login"
                else: type = ""
            else:
                text = ""
                type = ""
            return render(request, 'answer.html', {'info': info,'type':str(type)+" : "+str(text),'html':table_excel,'exist': 'Открыть старую таблицу'})

        except requests.exceptions.ConnectionError:
            info = "Потеряно соединение с сервером, повториите запрос"
            form = QueryForm()
            count = QueryCount()
            args = {'info':info,'form':form, 'count': count}
            return render(request, "main.html", args)
        except ValueError:
            info = "Открыта страница с нулевым поиском"
            form = QueryForm()
            count = QueryCount()
            args = {'info': info, 'form': form, 'count': count}
            return render(request, "main.html", args)
        except urllib.error.URLError:
            info = "Проблемы с подключением к интернету, проверьте его и повторите запрос"
            form = QueryForm()
            count = QueryCount()
            args = {'info': info, 'form': form, 'count': count}
            return render(request, "main.html", args)
        except:
            info = "Неопознанная ошибка, сообщите разработчику"
            form = QueryForm()
            count = QueryCount()
            args = {'info': info, 'form': form, 'count': count}
            return render(request, "main.html", args)


