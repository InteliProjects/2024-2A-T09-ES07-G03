import textwrap
import google.generativeai as genai
import os
import json

LLM_API_KEY = os.getenv("LLM_API_KEY")

termos_predefinidos_b3 = [
    "Regulamento",
    "Câmara",
    "Câmbio",
    "Fundos de investimento",
    "Postergação",
    "Market Data",
    "Contingência",
    "Certificação",
    "Comitentes",
    "Contratos futuros",
    "Cronograma",
    "tomador(es)",
    "Túneis",
    "doador(es)",
    "Opções",
    "Séries de opções",
    "Túneis de leilão",
    "Túneis de negociação",
    "Debentures",
    "Derivativos listados",
    "Listados",
    "Tarifação",
    "Dólar",
    "DI",
    "Epuma",
    "Feriado",
    "Futuro",
    "Garantia",
    "Garantias",
    "Garantias no Exterior",
    "Grandes lotes",
    "Gravames",
    "Ônus",
    "Horário",
    "Implementações previstas",
    "Limites de Posição em Aberto por Mercado",
    "Manual",
    "Manual de Administração de Risco da Câmara",
    "Mercado a vista",
    "Monitoriamento",
    "Negociação",
    "NoMe",
    "Novos Horários de Negociação",
    "oferta prioritária",
    "Ofertas diretas",
    "Ofertas públicas",
    "Operações estruturadas",
    "Plataforma NoMe",
    "PQO",
    "Privados",
    "PUMA",
    "PUMA Trading System",
    "Regras",
    "Regras de Liquidez",
    "Release",
    "Rolagem",
    "Tarifas",
    "Termo",
    "Tesouro Direto",
    "Trademante",
    "Ações",
    "Calendário",
    "empréstimo",
    "Parâmetros",
    "Pós-negociação",
    "Programa de Qualificação Operacional",
    "Renda Fixa",
    "Futuros",
    "Implementação",
    "Sessões de negociação",
    "Regras e Parâmetros de atuação",
    "Central Depositária"
]

# Classe para inicializar e definir o agente
class TagExtractorAgent():

    def __init__(self):        
        genai.configure(api_key=LLM_API_KEY)

        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def extract_tags(self, document_text): 

        if isinstance(document_text, list):
            document_text = "\n".join(document_text)

        # Gerar response a partir do prompt definido
        response = self.model.generate_content(
            textwrap.dedent(f"""
                O seu objetivo é ler um documento de regulamentações de órgãos reguladores do mercado financeiro e extrair 'tags' relacionadas às leis descritas no documento.

                OBRIGATORIAMENTE os itens da lista de output (tags) devem estar presentes no documento e ser coerentes com o conteúdo.

                Para extrair as tags, siga essa metodologia:
                1) Leia o documento inteiro e identifique as novas regulamentações.
                2) Para cada nova lei/regulamentação: extraia ao menos 1 tag relevante.
                3) SEMPRE leve em consideração as tags predefinidas: {termos_predefinidos_b3}
                4) Inclua tags das tags predefinidas caso se encaixem nesse cenário.
                4) Finalmente, responda de acordo com o #FormatoOutput.

                #FormatoOutput:
                Apenas retorne uma variável do tipo lista contendo tags relacionadas ao documento de entrada.
                Siga este exemplo de output:
                ['tag1', 'tag2', 'tag3', 'tag4', 'tag5']

                #IMPORTANTE: Apenas forneça a saída como uma lista JSON válida. Não inclua nenhuma explicação, texto adicional, ou qualquer outra coisa além da lista das tags.

                #Input:
                Abaixo está o texto do documento a ser analisado:
                {document_text}
            """),
            generation_config={'response_mime_type': 'application/json'}
        )


        # Extrai a lista de tags do objeto response
        try:
            tags_text = response._result.candidates[0].content.parts[0].text.upper()
            tags = json.loads(tags_text)
            return tags
        except (AttributeError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to extract tags from response: {e}")

# Teste 
if __name__ == "__main__":
    tagging_agent = TagExtractorAgent()

    document_text = """
        1
        INFORMAÇÃO PÚBLICA – PUBLIC INFORMATION
        Este documento produz efeitos a partir da data de sua publicação, respeitados os prazos específicos de vigência, se houver.
        O teor deste documento confere com o original assinado, disponível na B3.
        Praça Antonio Prado, 48 – 01010-901 – São Paulo, SP | Tel.: (11) 2565-5000.
        12 de setembro de 2024
        038/2024-VPC
        COMUNICADO EXTERNO
        Participantes do Listado B3
        Ref.: Alterações nas Políticas de Tarifação dos Produtos do Mercado a Vista
        de Renda Variável: Negociação e Pós-Negociação, Central Depositária
        Informamos que foi alterada a metodologia de Consolidação de Contas para
        composição do ADTV mensal e Saldo em Custódia, Operações de Leilão e
        Alocação por Preço Médio nas Políticas de Tarifação dos Produtos do Mercado a
        Vista de Renda Variável: Negociação e Pós-Negociação, Central Depositária,
        previstas no Comunicado Externo 030/2024-VPC de 25/07/2024.
        Desta forma, este Comunicado Externo visa republicar, em sua totalidade, as
        Políticas de Tarifação de Negociação e Pós-Negociação (Anexo I) e Central
        Depositária (Anexo II). As alterações estão previstas e consolidadas nos itens 3.1.1,
        3.1.5 e 5 do Anexo I e no item 1 do Anexo II.
        Serão mantidas as datas informadas para certificação no 4º trimestre de 2024 e
        previsão de implementação no 2º trimestre de 2025.
        A data de implementação das alterações relacionadas à negociação e central
        depositária será definida oportunamente, a depender do prazo necessário para
        adaptação dos participantes do mercado, e divulgada antecipadamente via Ofício
        Circular.
        2
        038/2024-VPC
        INFORMAÇÃO PÚBLICA – PUBLIC INFORMATION
        Este documento produz efeitos a partir da data de sua publicação, respeitados os prazos específicos de vigência, se houver.
        O teor deste documento confere com o original assinado, disponível na B3.
        Praça Antonio Prado, 48 – 01010-901 – São Paulo, SP | Tel.: (11) 2565-5000.
        As políticas de tarifação atuais para os produtos do mercado a vista de renda
        variável e para a central depositária permanecem válidas, conforme disposto no
        Ofício Circular 040/2024-PRE e no Ofício Circular 041/2024-PRE, respectivamente.
        Mais informações sobre o cronograma e especificações técnicas poderão ser
        consultadas em www.clientes.b3.com.br, Roadmap, Projetos, Nova Tarifação de
        Equities.
        Alterações realizadas no Anexo I
        Negociação e pós-negociação
        Serão realizadas as alterações descritas abaixo no modelo atual.
        • Item 3.1.1 Consolidação de contas para ADTV mensal: em complemento à
        divulgação anterior, informamos que o ADTV mensal para fins de
        determinação da tarifa de negociação passa a ser calculado através da
        consolidação de todas as contas de um mesmo documento (CPF, CNPJ ou
        terceiro bloco do documento CVM), independentemente do participante
        utilizado. Adicionalmente, mediante solicitação e apenas quando passível de
        comprovação através de base pública e regulatória (por exemplo, CVM, BCB),
        também será realizada a consolidação de mais de um documento pertencente
        ao mesmo grupo decisório (por exemplo, Gestora).
        Atenção: o grupo de documentos a serem consolidados no cálculo da taxa
        de negociação será o mesmo utilizado para fins do cálculo da taxa de custódia.
        • Item 3.1.5. Operações de leilão: atualmente, a tarifa calculada sobre
        operações realizadas nos leilões de abertura, fechamento e de oferta pública
        de aquisição (OPA) é diferenciada em relação àquelas fechadas em
        negociação regular. No novo modelo, serão diferenciadas apenas as
        operações realizadas nos leilões de abertura e fechamento, que seguem
        sendo tarifados a 0,0070%.
        • Item 5 (item novo na política). Alocação por preço médio: ressalta-se que
        será refletida no calculo da taxa média de negociação a tarifa calculada de
        acordo com as faixas da nova tabela.
        Alterações realizadas no Anexo II
        Central Depositária
        Serão realizadas alterações e aprimoramentos de texto descritos abaixo no
        modelo atual.
        • Tarifa de manutenção de conta: considerando a implementação da nova
        tarifa de custódia sobre o saldo total para todos os investidores, residentes e
        não residentes, a tarifa de manutenção de conta será extinta.
        • Item 1. Consolidação de contas para Valor em Custódia: em complemento
        à divulgação anterior, informamos que o Valor em Custódia para fins de
        determinação da tarifa da central depositária passa a ser calculado através da
        consolidação de todas as contas de um mesmo documento (CPF, CNPJ ou
        terceiro bloco do documento CVM), em um único custodiante.
        Adicionalmente, mediante solicitação e apenas quando passíveis de
        comprovação através de base pública e regulatória (por exemplo, CVM, BCB),
        também será realizada a consolidação de mais de um documento pertencente
        ao mesmo grupo decisório (por exemplo, Gestora).
        """
    tags = tagging_agent.extract_tags(document_text)

    print(tags)