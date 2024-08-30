from django.shortcuts import render
from django.contrib import messages
from decouple import config
import os
from openai import OpenAI
from dotenv import load_dotenv
# Create your views here.

def home(request):
    languages = ["c", "clike", "cpp", "csharp", "css", "css-extras", "csv", "django", "docker", "go", "graphql", "java", "javascript", "js-templates", "jsx", "kotlin", "lua", "markup", "markup-templating", "matlab", "mongodb", "php", "python", "r", "ruby", "rust", "scala", "sql", "typescript"]
    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']
        if lang == "Select Programming Language":
            messages.success(request, "Hey!, You Forgot To Select programming language")
            return render(request, 'home.html', {'languages': languages, 'lang': lang, 'code': code})
        
        return render(request, 'home.html', {'languages': languages, 'lang': lang, 'code': code})
    
    else:
        load_dotenv()
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"),)

        try:
            response = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": f"respond only with code. Fix this  code: ",
                    }
                ],
                model="gpt-3.5-turbo",
            )
            return render(request, 'home.html', {'languages': languages, 'response': response.choices[0].message['content']})
        except Exception as e:
            return render(request, 'home.html', {'languages': languages, 'response': str(e)})

    return render(request, 'home.html', {'languages': languages})