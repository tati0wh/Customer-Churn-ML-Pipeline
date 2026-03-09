# função para retirar coluna de id
def drop_unnecessary_columns(df):

    df = df.drop(columns=["Unnamed: 0"])

    return df

# função para retirar valores vazios de churn
def drop_missing_target(df):

    df = df.dropna(subset=["Churn"])

    return df

# função para substituir os nans da coluna 'genero' por 'Outros'
def fill_genero(df):
    df['genero'] = df['genero'].fillna('Outros')
    return df

# função para mapeamento para verificar se o registro de ausência de internet pode ser substituído pelo valor presente em outra coluna
def corrigir_servicos_internet(df):

    colunas_sem_internet = [
        'ServicoSegurancaCyber',
        'ServicoBackup',
        'SeguroDispositivos',
        'ServicoSuporteTecnico',
        'StreamingTV',
        'StreamingFilmes'
    ]

    condicao_nan = df[colunas_sem_internet].isna().any(axis=1)

    condicao_sem_servico = (
        (df['ServicoInternet'] == 'Sem serviço de internet') |
        (df[colunas_sem_internet] == 'Sem serviço de internet').any(axis=1)
    )

    condicao_servico_nao = df['ServicoInternet'] == 'Não'

    df.loc[condicao_nan & (condicao_sem_servico | condicao_servico_nao), colunas_sem_internet] = 'Não'

    df.loc[condicao_nan & ~(condicao_sem_servico | condicao_servico_nao), colunas_sem_internet] = 'Sem serviço de internet'

    return df

# mapeamento para verificar se o registro de ausência de serviço de telefone pode ser substituído pelo valor presente em outra coluna
def corrigir_servico_telefone(df):
    condicao_servico_telefone = (df['ServicoTelefone'] == 'Não') & (df['MultiLinhas'].isna())
    df.loc[condicao_servico_telefone, 'MultiLinhas'] = 'Sem serviço de telefone'

    condicao_multilinhas = (df['MultiLinhas'] == 'Sem serviço de telefone') & (df['ServicoTelefone'].isna())
    df.loc[condicao_multilinhas, 'ServicoTelefone'] = 'Não'

    return df

# preenche valores NaN nas colunas especificadas usando a moda
def preencher_nan_com_moda(df, colunas):
    for coluna in colunas:
        if coluna in df.columns:
            moda = df[coluna].mode()[0]
            df[coluna] = df[coluna].fillna(moda)

    return df

# transforma valores negativos em positivos em uma coluna
def corrigir_valores_negativos(df, coluna):
    df[coluna] = df[coluna].abs()
    return df

# preenche valores NaN de uma coluna com a média
def preencher_media(df, coluna):
    media = df[coluna].mean()
    df[coluna].fillna(media, inplace=True)
    return df

# normalização e seleção numerica
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

def encode_categorical_features(df):

    colunas_categoricas = [
        'genero',
        'MultiLinhas',
        'ServicoInternet',
        'ServicoSegurancaCyber',
        'ServicoBackup',
        'SeguroDispositivos',
        'ServicoSuporteTecnico',
        'StreamingTV',
        'StreamingFilmes',
        'Contrato',
        'MetodoPagamento'
    ]

    encoder = OneHotEncoder()

    encoded_data = encoder.fit_transform(df[colunas_categoricas])

    encoded_df = pd.DataFrame(
        encoded_data.toarray(),
        columns=encoder.get_feature_names_out(colunas_categoricas)
    )

    df = df.reset_index(drop=True)
    encoded_df = encoded_df.reset_index(drop=True)

    df_merged = pd.concat([df, encoded_df], axis=1)

    df_merged = df_merged.drop(columns=colunas_categoricas)

    return df_merged

# normalização e seleção numerica
from sklearn.preprocessing import Normalizer

def normalize_numeric_features(df):

    colunas_numericas_grandes = [
        'tempoDeServico',
        'FaturaMensal',
        'FaturaTotal',
        'NumTickets',
        'NumTicketsTecnico'
    ]

    normalizer = Normalizer()

    df[colunas_numericas_grandes] = normalizer.fit_transform(
        df[colunas_numericas_grandes]
    )

    return df