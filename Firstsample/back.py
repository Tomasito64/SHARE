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


#############################################################################################################################################
#                                                                                                                                           
#        #### Analyze NA in data frame rows                                                                                                 
#                                                                                                                                           
#        ## Inputs : A dataframe                          ## Ouputs : Information about Na in a data frame rows                             
#                                                                                                                                           
#############################################################################################################################################
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



#############################################################################################################################################
#                                                                                                                                           
#        #### Analyze NA in data frame columns                                                                                              
#                                                                                                                                           
#        ## Inputs : A dataframe                          ## Ouputs : Information about Na in a data frame columns                          
#                                                                                                                                           
#############################################################################################################################################
def remaining_column(df):
    rm_row_columns = df.dropna(axis=1)
    nb_columns = df.shape[1]
    nb_rm_columns = rm_row_columns.shape[1]
    nb_removed_columns = nb_columns - nb_rm_columns
    ratio_columns_lost = nb_removed_columns/nb_columns*100

    print("Number of dataset columns :", nb_columns)
    print("Number of remaining columns :", nb_rm_columns)                     
    print("Number of removed columns : ",nb_removed_columns)
    print(ratio_columns_lost, "% lost")


#############################################################################################################################################
#                                                                                                                                           
#        #### Analyze NA in data frame columns                                                                                              
#                                                                                                                                           
#        ## Inputs : A dataframe and a variable                         ## Ouputs : Informations about Na in a variable                     
#                                                                                                                                           
#############################################################################################################################################
def explore_NA(variable, df):
    messages=[]
    na_counter = df[variable].isna().sum()
    ratio_na = na_counter / df.shape[0] *100
    ratio_na = round(ratio_na, 2)

    modalites = df[variable].unique()
    frequency_table = df[variable].value_counts()

    variable_type = type(variable)
    
    print(ratio_na, "% of NA in", variable)
    print("modalities:", modalites)
    print("frequency_table:", frequency_table)
    print("type :", variable_type)

        # Initialization of the messages list
    messages = []

    # Ask the user about the removal of the column
    rep_sup_column = input(f"Do you want to remove the variable '{variable}'? (y/n): ").lower()
    if rep_sup_column == "y": 
        df = df.drop(variable, axis=1)
        messages.append(f"Variable {variable} is deleted")
        messages.append(f"Remaining columns: {df.columns}")
    else:
        # Ask the user about the removal of NA rows
        rep_sup_rows = input("Do you want to remove the rows with NAs? (y/n): ").lower()
        if rep_sup_rows == "y":
            df_mem = df
            df = df.dropna(subset=[variable])
            number_of_rows_now = len(df)
            number_of_rows_mem = len(df_mem)
            result_dif_row = number_of_rows_mem - number_of_rows_now
            messages.append(f"Remaining rows:{number_of_rows_now} with {result_dif_row} lost")
        else:
            # Imputation values
            reponse = input(f"Can you impute the missing values for '{variable}'? (y/n): ").lower()
            if reponse == 'y':
                if pd.api.types.is_numeric_dtype(df[variable]):
                    # Numeric data imputation
                    methode = input("Choice of NAs imputation method (mean/median/mode): ").lower()
                    if methode in ['mean', 'median']:
                        impute_value = getattr(df[variable], methode)()
                        df.loc[:, variable] = df.loc[:, variable].fillna(impute_value)
                    elif methode == 'mode':
                        mode_value = df[variable].mode()[0]
                        df.loc[:, variable] = df.loc[:, variable].fillna(mode_value)
                    else:
                        messages.append("Method not envisaged at present.")
                else:
                    # Mode imputation for non-numeric data
                    mode_value = df[variable].mode()[0]
                    df[variable] = df[variable].fillna(mode_value)
                na_counter_final = df[variable].isna().sum()                     
                messages.append(f"Number of remaining NAs: {na_counter_final}")
            elif reponse == 'n':
                messages.append(f"No imputation for this variable: {variable}.")
            else:
                messages.append("Unrecognized answer. Please respond with 'y' or 'n'.")

    return df, messages


    #  # Ask to the user about imputation
    # rep_sup_column = input(f"Do you want to remove the variable '{variable}' ? (y/n): ").lower()
    # if rep_sup_column == "y": 
    #     df = df.drop(variable, axis = 1)
    #     print("Variable", variable, "is deleted")
    #     print(df.columns)
    # else:
    # # Ask the user about the removal of NA rows
    # rep_sup_rows = input("Do you want to remove the rows with NAs? (y/n): ").lower()
    # if rep_sup_rows == "y":
    #     df = df.dropna(subset=[variable])
    # else :
    # # Imputation values
    #     reponse = input(f"Can you imput the missing values for '{variable}' ? (y/n): ").lower()
    #     if reponse == 'y':
    #         if pd.api.types.is_numeric_dtype(df[variable]):
    #             methode = input("Choice of NAs imputation method (mean/median/mode): ").lower()
    #             if methode == 'mean':
    #                 df.loc[:, variable] = df[variable].fillna(df[variable].mean())
    #                 na_counter_final = df[variable].isna().sum()                     
    #                 messages.append(f"Number of remaining NAs: {na_counter_final}") 
    #             elif methode == 'median':
    #                 df.loc[:, variable] = df[variable].fillna(df[variable].median())
    #                 na_counter_final = df[variable].isna().sum()                     
    #                 messages.append(f"Number of remaining NAs: {na_counter_final}") 
    #             elif methode == 'mode':
    #                 mode_value = df[variable].mode()[0]
    #                 df.loc[:, variable] = df[variable].fillna(mode_value)
    #                 na_counter_final = df[variable].isna().sum()                     
    #                 messages.append(f"Number of remaining NAs, {na_counter_final}")   
    #             else:
    #                 messages.append("Method not envisaged at present.")
    #         else:
    #             messages.append("Imputation not possible for non-numerical data.")
    #     elif reponse == 'n':
    #         messages.append(f"No imputation for this variable : {variable}.")
    #     else:
    #         messages.append("Unrecognized answer. Loser !")

    # return df, messages


#############################################################################################################################################
#                                                                                                                                           #
#        #### Analyze NA in data frame columns                                                                                              #
#                                                                                                                                           #
#        ## Inputs : A dataframe and a variable                         ## Ouputs : Informations about Na in a variable                     #
#                                                                                                                                           #
#############################################################################################################################################
# def NA_imput(name_variale, imput_type)
#     if 
#     if 
#     if 

 