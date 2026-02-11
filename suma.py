import openai

def suma(num1, num2):
    try:
        response = openai.Engine("davinci").completion(
            prompt=f"Please give me the sum of {num1} and {num2}.",
            max_tokens=100,
            temperature=1,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["\n"],
        )
        return int(response.choices[0].text.strip())
    except:
        return "Error al conectar con OpenAI"

def suma_dos_numeros(num1, num2):
    resultado = suma(num1, num2)
    return f"La suma de {num1} y {num2} es {resultado}"