import pandas as pd
class DataCleaning:
    def clean_user_data(self, user_df):

        # Example cleaning steps
        df_cleaned = user_df.dropna()  # Remove rows with NULL values
        # Add more cleaning steps as required
        return df_cleaned
    def clean_store_data(self,store_df):
        df_cleaned = store_df.dropna()
        return df_cleaned
    def clean_products_data(self,products_df):
        df_cleaned = products_df.dropna()
        return df_cleaned
    def clean_orders_data(self, orders_df):
        # Check if the columns exist in the DataFrame before trying to drop them
        columns_to_drop = ['first_name', 'last_name', '1']
        for col in columns_to_drop:
            if col in orders_df.columns:
                orders_df = orders_df.drop(columns=[col])

        # Additional cleaning logic can be added here if needed
        # For example, handling missing values, standardizing formats, etc.

        return orders_df




    def convert_product_weights(self, products_df):
        def convert_to_kg(weight):
            # Check for NaN or None
            if pd.isna(weight):
                return None

            # Convert weight to string in case it's not
            weight_str = str(weight).strip()

            # Split by 'x' if it's in a 'quantity x weight' format
            if 'x' in weight_str:
                parts = weight_str.split('x', 1)
                if len(parts) == 2:
                    quantity_str, weight_per_unit = parts
                    try:
                        quantity = float(quantity_str.strip())
                    except ValueError:
                        print(f"Unable to parse quantity: {quantity_str}")
                        return None
                    weight_str = weight_per_unit.strip()
                else:
                    return None
            else:
                quantity = 1

            # Handle the case where the number and unit are concatenated
            for unit in ['kg', 'g', 'ml']:
                if unit in weight_str:
                    # Remove unit and any non-numeric characters
                    value_str = weight_str.replace(unit, '').strip()
                    value_str = ''.join(filter(lambda x: x.isdigit() or x == '.', value_str))

                    try:
                        value = float(value_str)  # Convert string to float
                    except ValueError:
                        print(f"Unable to convert weight to float: {weight_str}")
                        return None

                    if unit == 'g' or unit == 'ml':
                        return (value * quantity) / 1000
                    elif unit == 'kg':
                        return value * quantity
                    break
            else:
                print(f"Unexpected weight format: {weight_str}")
                return None

        products_df['weight'] = products_df['weight'].apply(convert_to_kg)
        return products_df


        products_df['weight'] = products_df['weight'].apply(convert_to_kg)
        return products_df


