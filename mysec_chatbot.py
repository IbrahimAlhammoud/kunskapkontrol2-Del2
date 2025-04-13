import os
from dotenv import load_dotenv
import openai
import requests
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

# Ladda miljövariabler från .env-filen
load_dotenv()

# Sätt din OpenAI API-nyckel
openai.api_key = os.getenv("OPENAI_API_KEY")

# Skapa LangChain-LLM-objektet
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=openai.api_key)

# Skapa en enkel prompt för att formatera användarens fråga
prompt = PromptTemplate(input_variables=["question"], template="You are a helpful assistant. Answer the following question: {question}")

# Skapa LangChain-kedja med LLM
chain = LLMChain(llm=llm, prompt=prompt)

# Funktion för att generera svar från GPT-4 med LangChain
def generate_answer_with_langchain(question: str):
    response = chain.run({"question": question})
    return response

# Funktion för att göra ett HTTP-anrop till OpenAI API med Requests
def generate_answer_with_requests(question: str):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openai.api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(url, json=data, headers=headers)
    
    if response.status_code == 200:
        return response.json()['choices'][0]['message']['content'].strip()
    else:
        return f"Error: {response.status_code} - {response.text}"

# Funktion som simulerar Mysec:s FAQ och hanterar besiktning, felanmälan, etc.
def mysec_faq(question: str):
    faq_data = {
    "besiktning": "För att göra en besiktning, vänligen fyll i formuläret på vår webbplats...",
    "felanmälan": "För att göra en felanmälan, vänligen fyll i formuläret med information...",
    "brandlarm": "Mysec är certifierad för att installera och underhålla brandlarm...",
    "inbrottslarm": "Mysec erbjuder installation och service av inbrottslarm...",
    "kameraövervakning": "Mysec är certifierad för CCTV-installation...",
    "kontakt": "Du kan kontakta Mysec på +46 8 775 42 60 eller kontakt@mysec.se...",
    "företagspresentation": "Mysec Sweden AB erbjuder säkerhetslösningar såsom inbrottslarm...",
    "kvalitet": "Mysec strävar efter att leverera högsta kvalitet i alla våra tjänster...",
    "policy": "Mysec har en strikt policy för kvalitet och arbetsmiljö...",
    "larmportal": "MYSEC Larmportal är ett molnbaserat system där du som behörig användare...",
    "jour": "Vår jourtjänst innebär att du alltid har tillgång till teknisk personal...",
    "kamera": "Mysec erbjuder CCTV-installation med certifierade tekniker...",
    "service": "Vi erbjuder service och underhåll enligt ISO-certifierade rutiner...",
    "säkerhet": "Mysec erbjuder helhetslösningar inom säkerhet...",
    "miljöpolicy": "Vi arbetar aktivt för att minska vår miljöpåverkan...",
    "jobba hos": "Vi söker alltid nya talanger. Kolla in våra lediga tjänster...",
    "tjänster": "Vi erbjuder brandlarm, inbrottslarm, lås, passersystem, kameraövervakning och jourtjänster.",
    "kontaktuppgifter": "Du kan nå oss via telefon +46 8 775 42 60 eller e-post kontakt@mysec.se.",
    "lediga jobb": "vi söker just nu erfaren tekniker inom brandlarm och inbrottslarm, fyll i nedan förmula och skicka till oss",
    "adress": "Västberga allé 60 126 30 Hägersten"
}


    # Kollar om användarens fråga matchar några specifika kategorier
    for key in faq_data:
        if key.lower() in question.lower():
            return faq_data[key]
    
    # Om inga specifika matchningar finns, använd LangChain för att generera ett generellt svar
    return generate_answer_with_langchain(question)

