#Script do Projeto 1 utilizando PANDAS.
#Importa
import pandas as pd
import matplotlib.pyplot as plt

print("\n Abrindo arquivo...\n"), print("."), print("."), print("."), print(".")
#Lê o arquivo .csv
df = pd.read_csv("chicago.csv")
print(df.head()) #Printa as primeiras 5 linhas

print("As colunas são: ",df.columns)
input("\nPressione enter para continuar..\n")
print("\n\n Analisando os tipos de dados... \n\n")
#Informações sobre os dados
print(df.info())
#Podemos ver que existem dados faltantes.

input("\nPressione enter para continuar..\n")
print("\n\n Substituindo os dados faltantes em Birth Year pela média...")
#Substitui os dados faltantes em 'birthday year' pela média deste
by_mean = df["Birth Year"].mean() #Média
df["Birth Year"] = df["Birth Year"].fillna(by_mean) #Preenche os dados faltantes com média.
print(df.info())

input("\n\nPressione enter para continuar...\n")
print(df.describe())


print("\nPegando apenas os dados do dia 01/01/2017 das 00h até 00:59...")
#Pega apenas os dados do dia 01/01/2017 das 00h até 00:59.
fevereiro = df[(df['Start Time'] >= '2017-01-01 00:00:36') &
            (df['Start Time'] <= '2017-01-01 00:59:00')]
print(fevereiro)

input("\n\nPressione enter para continuar...\n\n")
#Print na soma de trip duration
print("\n\nA soma das Trip Duration deste horário é: {}.\n\n"
    .format(fevereiro['Trip Duration'].sum()))

#Print data e horário de inicio e término da maior viagem registrada no dia e
#hora estudado.
print("\n\nPressione enter para continuar...\n\n")
max_trip_fevereiro = fevereiro['Trip Duration'].idxmax()

print("O horário de início em que teve a maior duração de viagem foi: {}."
    .format(df.iloc[max_trip_fevereiro]['Start Time']))
print("O horário de término em que teve a maior duração de viagem foi: {}"
    .format(df.iloc[max_trip_fevereiro]['End Time']))

def busca_user(idx):
    """Função que retorna o tipo de usuário buscado pelo índice
    idx: índice da linha

    """
    if df.iloc[idx]['User Type'] == 'Subscriber':
        return("Este usuário era 'Subscriber'.")

    elif df.iloc[idx]['User Type'] == 'Customer':
        return("Este usuário era 'Customer'.")


def busca_gender(idx):
    """Função que retorna o gênero do usuário buscado pelo índice
    idx: índice da linha

    """
    if df.iloc[idx]['Gender'] == 'Female':
        return("Este usuário era mulher.\n\n")

    elif df.iloc[idx]['Gender'] == 'Male':
        return("Este usuário era homem.\n\n")


print(busca_user(max_trip_fevereiro))
print(busca_gender(max_trip_fevereiro))

#Print data e horário de inicio e término da menor viagem registrada no dia e hora estudado.
min_trip_fevereiro = fevereiro['Trip Duration'].idxmin()
print("O horário de início em que teve a menor duração de viagem foi: {}."
    .format(df.iloc[min_trip_fevereiro]['Start Time']))
print("O horário de término em que teve a menor duração de viagem foi: {}."
    .format(df.iloc[min_trip_fevereiro]['End Time']))

print(busca_user(min_trip_fevereiro))
print(busca_gender(min_trip_fevereiro))

#Calculando a média dos dados para cada tipo de user.
input("\n\nAperte enter para continuar...\n")
print("Calculando a média de trip duration e birth year para cada user type...\n")
print(df.groupby("User Type").mean())

input("\n\nAperte enter para continuar...")
print("\n\nCriando uma nova coluna 'Duração' através do cut()...")
#Criando uma nova coluna que determina a duração usando .cut()
bin_edges = [6, 392, 670, 1127, 8633] #Valores limites de borda = min, 25%, 50%, 75% e max
bin_labels = ["Baixa duração", "Moderadamente Baixa", "Moderadamente Alta", "Alta"]
df["Duração"] = pd.cut(df["Trip Duration"], bin_edges, labels=bin_labels) #Cria nova coluna.
print(df.head())

input("\n\nAperte enter para continuar...")
print("\n\nAgrupando a média de TD e BY por Duração...")
#Agrupa por groupby a média em duração.
print(df.groupby("Duração").mean())

input("\n\nAperte enter para continuar...")
print("\n\nCalculando a mediana de Birth Year e pegando linhas > mediana...")
#Calculando a mediana de Birth Year e pegando apenas BY > mediana
print("\nA mediana de Birth Year é: {}".format(df["Birth Year"].median()))
median_bf = df["Birth Year"].median()
m = df[(df["Birth Year"] > median_bf)]
print(m.head())

input("\n\nAperte enter para continuar...")
print("\n\nRenomeando Birth Year para BirthYear...")
#Renomeando coluna "Birth Year" para poder usar query
df = df.rename(index=str, columns={'Birth Year': 'BirthYear'})
print(df.head())

#Agrupando dados usando query
input("\n\nAperte enter para continuar...")
print("\nPegando todos Birth Year acima de 1990...")
by = df.query('BirthYear > 1990.0')
print(by.head())

input("Aperte enter para continuar...")
#Agrupando pela Duração a média de BirthYear
print("\n\nAgrupando para cada Duração as médias de Birth Year...")
caso1 = df.groupby("Duração").mean()["BirthYear"]
print(caso1)

input("\n\nAperte enter para continuar...")
print("\n\nCriando gráfico...")
#Colocando em uma variável a média de BY de cada duração
baixa = caso1["Baixa duração"]
mod_baixa = caso1["Moderadamente Baixa"]
mod_alta = caso1["Moderadamente Alta"]
alta = caso1["Alta"]

#Criando o gráfico
loc = [1, 2, 3, 4]
altura = [mod_baixa, baixa, mod_alta, alta]
labels = ['Mod Baixa', 'Baixa', 'Mod Alta', 'Alta']
plt.bar(loc, altura, tick_label=labels)
plt.title("Média de Ano de Nascimento Comparado à Duração", fontsize=18)
plt.xlabel("Duração", fontsize=18)
plt.ylabel("Birth Year", fontsize=18)
plt.show(block=True)

input("\n\nAperte enter para continuar...\n")
print("Separando as amostras com Trip Duration >= mediana.\n\n")
#Renomeando a columa Trip Duration para poder usar o método .query()
df = df.rename(index=str, columns={'Trip Duration': 'Trip_Duration'})
mediana_trip = df["Trip_Duration"].median()
duracao_300 = df.query('Trip_Duration >= @mediana_trip')
print(duracao_300["Trip_Duration"].head())

customer_duracao = []
subscriber_duracao =[]
for tipo in duracao_300["User Type"]:
    if tipo == 'Customer':
        customer_duracao.append(tipo)
    elif tipo == 'Subscriber':
        subscriber_duracao.append(tipo)

if len(customer_duracao) > len(subscriber_duracao):
    print("A maioria dos usuários do intervalo de Trip Duration > 300 é {} com: {}"
        .format('Customer', len(customer_duracao)))
else:
    print ("A maioria dos uruários é Subscriber com: {}".
        format(len(subscriber_duracao)))
