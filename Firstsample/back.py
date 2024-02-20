##############################################################
#                                                            #
#   FFFFFF  U   U  N   N   CCCC  TTTTTT  III   O O   N   N   #
#   FF      U   U  NN  N  CC  CC   TT     I   O   O  NN  N   #
#   FFFF    U   U  N N N  CC       TT     I   O   O  N N N   #
#   FF      U   U  N  NN  CC  CC   TT     I   O   O  N  NN   #
#   FF       UUU   N   N   CCCC    TT    III   O O   N   N   #
#                                                            #
##############################################################

#### IPPORTS

import pandas as pd


##################################################################################################################################################################################################
#                                                                                                                                           
#        #### Analyze NA in data frame rows                                                                                                 
#                                                                                                                                           
#        ## Inputs : A dataframe                          ## Ouputs : Information about Na in a data frame rows                             
#                                                                                                                                           
##################################################################################################################################################################################################
def remaining_rows(df):
    rm_rows  = df.dropna()
    nb_rows = df.shape[0]
    nb_rm_rows = rm_rows.shape[0]
    nb_removed_rows = nb_rows - nb_rm_rows
    ratio_rows_lost = nb_removed_rows/nb_rows*100
    ratio_rows_lost = round(ratio_rows_lost, 2)

    print("Number of dataset rows :", nb_rows)
    print("Number of remaining rows :", nb_rm_rows)
    print("Number of removed rows : ", nb_removed_rows)
    print(ratio_rows_lost, "% lost")



##################################################################################################################################################################################################
#                                                                                                                                           
#        #### Analyze NA in data frame columns and propose solutions to deal with them                                                                                       
#                                                                                                                                           
#        ## Inputs : A dataframe ; avariable name ; dictionary         ## Ouputs : Information about Na in a data frame columns and proposals to deal with them                  
#                                                                                                                                           
##################################################################################################################################################################################################
def explore_NA(variable, df, answers=None):
    if answers is None:
        answers = {}  # Si aucun dictionnaire de réponses n'est fourni, utilisez un dictionnaire vide

    na_counter = df.loc[:, variable].isna().sum()
    ratio_na = na_counter / df.shape[0] * 100
    ratio_na = round(ratio_na, 2)

    modalites = df.loc[:, variable].unique()
    frequency_table = df.loc[:, variable].value_counts()

    variable_type = type(variable)
    
    print(f"{ratio_na}% of NA in {variable}")
    print("modalities:", modalites)
    print("frequency_table:", frequency_table)
    print("type :", variable_type)

    messages = []

    # Utilisez le dictionnaire de réponses si disponible, sinon demandez à l'utilisateur
    rep_sup_column = answers.get('rep_sup_column', input(f"Do you want to remove the variable '{variable}'? (y/n): ").lower())
    if rep_sup_column == "y":
        df = df.drop(variable, axis=1)
        messages.append(f"Variable {variable} is deleted")
        messages.append(f"Remaining columns: {list(df.columns)}")
    else:
        rep_sup_rows = answers.get('rep_sup_rows', input("Do you want to remove the rows with NAs? (y/n): ").lower())
        if rep_sup_rows == "y":
            df_mem = df.copy()
            df = df.dropna(subset=[variable])
            number_of_rows_now = len(df)
            number_of_rows_mem = len(df_mem)
            result_dif_row = number_of_rows_mem - number_of_rows_now
            messages.append(f"Remaining rows: {number_of_rows_now} with {result_dif_row} lost")
        else:
            reponse = answers.get('reponse', input(f"Can you impute the missing values for '{variable}'? (y/n): ").lower())
            if reponse == 'y':
                if pd.api.types.is_numeric_dtype(df.loc[:, variable]):
                    method = answers.get('method', input("Choice of NAs imputation method (mean/median/mode): ").lower())
                    if method in ['mean', 'median']:
                        impute_value = getattr(df.loc[:, variable], method)()
                        df.loc[:, variable] = df.loc[:, variable].fillna(impute_value)
                    elif method == 'mode':
                        mode_value = df.loc[:, variable].mode()[0]
                        df.loc[:, variable] = df.loc[:, variable].fillna(mode_value)
                    else:
                        messages.append("Method not envisaged at present.")
                else:
                    mode_value = df.loc[:, variable].mode()[0]
                    df.loc[:, variable] = df.loc[:, variable].fillna(mode_value)
                na_counter_final = df.loc[:, variable].isna().sum()                     
                messages.append(f"Number of remaining NAs: {na_counter_final}")
            elif reponse == 'n':
                messages.append(f"No imputation for this variable: {variable}.")
            else:
                messages.append("Unrecognized answer. Please respond with 'y' or 'n'.")

    return df, messages



################################################################################################################################################################################################
#                                                                                                                                           
#        #### Analyze NA in data frame columns and propose solutions to deal with them (Automatic)                                                                                      
#                                                                                                                                           
#        ## Inputs : A dataframe ; avariable name ; dictionary         ## Ouputs : Information about Na in a data frame columns and proposals to deal with them                  
#                                                                                                                                           
##################################################################################################################################################################################################
def explore_NA_auto(variable, df, answers=None):
    if answers is None:
        answers = {}  # Si aucun dictionnaire de réponses n'est fourni, utilisez un dictionnaire vide.

    # Calcul du pourcentage de valeurs manquantes pour la variable.
    na_counter = df.loc[:, variable].isna().sum()
    ratio_na = na_counter / df.shape[0] * 100
    ratio_na = round(ratio_na, 2)

    # Affichage des informations de base sur les valeurs manquantes.
    print(f"{ratio_na}% of NA in {variable}")
    print("Modalities:", df.loc[:, variable].unique())
    print("Frequency table:", df.loc[:, variable].value_counts())
    print("Type:", df.loc[:, variable].dtype)

    messages = []

    # Décision de suppression de la colonne.
    rep_sup_column = answers.get('rep_sup_column', 'n').lower()
    if rep_sup_column == "y":
        df = df.drop(columns=[variable])
        messages.append(f"Variable {variable} is deleted")
        messages.append(f"Remaining columns: {list(df.columns)}")
    else:
        # Décision de suppression des lignes contenant des valeurs manquantes.
        rep_sup_rows = answers.get('rep_sup_rows', 'n').lower()
        if rep_sup_rows == "y":
            before_rows = df.shape[0]
            df = df.dropna(subset=[variable])
            after_rows = df.shape[0]
            messages.append(f"Rows before: {before_rows}, after: {after_rows}, {before_rows - after_rows} rows removed.")
        else:
            # Décision d'imputation des valeurs manquantes.
            reponse = answers.get('reponse', 'n').lower()
            if reponse == 'y':
                method = answers.get('method', 'mode').lower()
                if method == 'mean' and pd.api.types.is_numeric_dtype(df[variable]):
                    impute_value = df[variable].mean()
                elif method == 'median' and pd.api.types.is_numeric_dtype(df[variable]):
                    impute_value = df[variable].median()
                elif method == 'mode':
                    impute_value = df[variable].mode()[0]
                else:
                    impute_value = None
                    messages.append("No suitable imputation method found.")
                if impute_value is not None:
                    # Correcte modification pour éviter le SettingWithCopyWarning.
                    df[variable] = df[variable].fillna(impute_value)
                    messages.append(f"{variable} imputed with {method} value: {impute_value}.")
                    na_counter_final = df[variable].isna().sum()
                    messages.append(f"Number of remaining NAs: {na_counter_final}")
            else:
                messages.append(f"No action taken for {variable}.")

    return df, messages

###### Merge the two functions : if respond so... in the other hand, ask to the user