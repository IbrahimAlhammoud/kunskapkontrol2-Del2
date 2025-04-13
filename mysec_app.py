import streamlit as st
from mysec_chatbot import mysec_faq
import smtplib
from email.mime.text import MIMEText

# Funktion för att skicka e-post
def send_email(subject, body, to_email):
    from_email = "your-email@example.com"
    email_password = "your-email-password"

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP_SSL('smtp.example.com', 465)
        server.login(from_email, email_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        st.success("📧 Formuläret har skickats!")
    except Exception as e:
        st.error(f"❌ Fel vid e-postskickning: {str(e)}")

# Streamlit App
st.title("💬 Mysec Chatbot")

st.write("Ställ gärna din fråga till vår chatbot:")

user_question = st.text_input("Skriv din fråga här:")

if user_question:
    # Svar från chatbot
    answer = mysec_faq(user_question)
    st.write(f"**Svar från chatbot:** {answer}")

    question_lower = user_question.lower()

    # Besiktning
    if "besiktning" in question_lower:
        with st.form("besiktning_form"):
            st.write("**📋 Besiktning:** Fyll i formuläret nedan.")
            location = st.text_input("Plats för besiktning:")
            date = st.date_input("Datum:")
            time = st.time_input("Tid:")
            number_of_people = st.number_input("Antal personer:", min_value=1, max_value=100)
            submitted = st.form_submit_button("Skicka förfrågan")

            if submitted:
                form_data = f"""
                🏢 Besiktning begäran:
                Plats: {location}
                Datum: {date}
                Tid: {time}
                Antal personer: {number_of_people}
                """
                send_email("Besiktning Förfrågan", form_data, "kontakt@mysec.se")

    # Felanmälan
    elif "felanmälan" in question_lower:
        with st.form("felanmalan_form"):
            st.write("**🛠️ Felanmälan:** Fyll i formuläret nedan.")
            obj = st.text_area("Objekt namn eller nummer:")
            description = st.text_area("Beskriv felet:")
            time_of_issue = st.time_input("Tidpunkt för felet:")
            submitted = st.form_submit_button("Skicka felanmälan")

            if submitted:
                form_data = f"""
                🛠️ Felanmälan:
                Objekt: {obj}
                Beskrivning: {description}
                Tidpunkt: {time_of_issue}
                """
                send_email("Felanmälan", form_data, "kontakt@mysec.se")

    # Besök
    elif "besök" in question_lower:
        with st.form("besok_form"):
            st.write("**📅 Besökning:** Fyll i formuläret nedan.")
            purpose = st.text_input("Syftet med besökning:")
            date = st.date_input("Datum:")
            time = st.time_input("Tid:")
            number_of_people = st.number_input("Antal personer:", min_value=1, max_value=100)
            submitted = st.form_submit_button("Skicka besöksbokning")

            if submitted:
                form_data = f"""
                📅 Besök:
                Syfte: {purpose}
                Datum: {date}
                Tid: {time}
                Antal personer: {number_of_people}
                """
                send_email("Besök Bokning", form_data, "kontakt@mysec.se")

    # Lediga jobb
    elif "lediga jobb" in question_lower or "jobb" in question_lower:
        st.write("**💼 Lediga jobb:**")

        experience = st.radio("Har du erfarenhet inom Brandlarm eller Inbrottslarm?", ["Ja", "Nej"])

        if experience == "Ja":
            with st.form("job_application_form"):
                st.write("Bra! Fyll i formuläret nedan.")
                years = st.number_input("Antal år erfarenhet", min_value=0, step=1)
                name = st.text_input("Ditt namn")
                age = st.number_input("Din ålder", min_value=15, max_value=100)
                email = st.text_input("E-post")
                submitted = st.form_submit_button("Skicka ansökan")

                if submitted:
                    form_data = f"""
                    💼 Jobbansökan:
                    Namn: {name}
                    Ålder: {age}
                    E-post: {email}
                    Erfarenhet: {years} år
                    """
                    send_email("Anställning Förfrågan", form_data, "kontakt@mysec.se")
                    st.success(f"📝 Tack {name}, vi kontaktar dig snarast möjligt.")
        else:
            st.info("⚠️ Just nu söker vi endast erfarna medarbetare. Återkom gärna senare.")
