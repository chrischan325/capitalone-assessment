from itertools import permutations
import streamlit as st
import pandas as pd


def calculate_rewards(transactions):
    sportcheck_amount = 0
    tim_hortons_amount = 0
    subway_amount = 0
    other_amount = 0
    transaction_map = {}

    for transaction_id, transaction in transactions.items():
        merchant = transaction["merchant_code"]
        amount = transaction["amount_cents"]

        transaction_map[transaction_id] = calculate_transaction_reward(merchant, amount)

        sportcheck_amount += amount if merchant == "sportcheck" else 0
        tim_hortons_amount += amount if merchant == "tim_hortons" else 0
        subway_amount += amount if merchant == "subway" else 0
        other_amount += amount if merchant not in ["sportcheck", "tim_hortons", "subway"] else 0

    perms = [''.join(p) for p in permutations('1234567')]
    max_reward = 0

    for perm in perms:
        temp_sportcheck = sportcheck_amount
        temp_timhortons = tim_hortons_amount
        temp_subway = subway_amount
        temp_other = other_amount
        temp_points = 0
        for c in perm:
            if c == '1':
                apply = min(temp_sportcheck // 7500, temp_timhortons // 2500, temp_subway // 2500)
                temp_points += 500 * apply
                temp_sportcheck -= 7500 * apply
                temp_timhortons -= 2500 * apply
                temp_subway -= 2500 * apply
            elif c == '2':
                apply = min(temp_sportcheck // 7500, temp_timhortons // 2500)
                temp_points += 300 * apply
                temp_sportcheck -= 7500 * apply
                temp_timhortons -= 2500 * apply
            elif c == '3':
                apply = temp_sportcheck // 7500
                temp_points += 200 * apply
                temp_sportcheck -= 7500 * apply
            elif c == '4':
                apply = min(temp_sportcheck // 2500, temp_timhortons // 1000, temp_subway // 1000)
                temp_points += 150 * apply
                temp_sportcheck -= 2500 * apply
                temp_timhortons -= 1000 * apply
                temp_subway -= 1000 * apply
            elif c == '5':
                apply = min(temp_sportcheck // 2500, temp_timhortons // 1000)
                temp_points += 75 * apply
                temp_sportcheck -= 2500 * apply
                temp_timhortons -= 1000 * apply
            elif c == '6':
                apply = temp_sportcheck // 2000
                temp_points += 75 * apply
                temp_sportcheck -= 2000 * apply
            elif c == '7':
                apply = sum([temp_sportcheck, temp_timhortons, temp_subway, temp_other]) // 100
                temp_points += 1 * apply
                break
        if max_reward < temp_points:
            max_reward = temp_points

    return max_reward, transaction_map


def calculate_transaction_reward(merchant, amount):
    sportcheck_amount = amount if merchant == "sportcheck" else 0
    tim_hortons_amount = amount if merchant == "tim_hortons" else 0
    subway_amount = amount if merchant == "subway" else 0
    other_amount = amount if merchant not in ["sportcheck", "tim_hortons", "subway"] else 0

    points = 0

    while sportcheck_amount >= 7500:
        points += 200
        sportcheck_amount -= 7500

    while sportcheck_amount >= 2000:
        points += 75
        sportcheck_amount -= 2000

    points += sum([sportcheck_amount + tim_hortons_amount + subway_amount + other_amount]) // 100
    return points


if __name__ == '__main__':
    test_transactions1 = {
        "T01": {"date": "2021-05-01", "merchant_code": "sportcheck", "amount_cents": 21000},
        "T02": {"date": "2021-05-02", "merchant_code": "sportcheck", "amount_cents": 8700},
        "T03": {"date": "2021-05-03", "merchant_code": "tim_hortons", "amount_cents": 323},
        "T04": {"date": "2021-05-04", "merchant_code": "tim_hortons", "amount_cents": 1267},
        "T05": {"date": "2021-05-05", "merchant_code": "tim_hortons", "amount_cents": 2116},
        "T06": {"date": "2021-05-06", "merchant_code": "tim_hortons", "amount_cents": 2211},
        "T07": {"date": "2021-05-07", "merchant_code": "subway", "amount_cents": 1853},
        "T08": {"date": "2021-05-08", "merchant_code": "subway", "amount_cents": 2153},
        "T09": {"date": "2021-05-09", "merchant_code": "sportcheck", "amount_cents": 7326},
        "T10": {"date": "2021-05-10", "merchant_code": "tim_hortons", "amount_cents": 1321}
    }

    test_transactions2 = {
        'T1': {'date': '2021-05-09', 'merchant_code': 'sportcheck', 'amount_cents': 7326},
        'T2': {'date': '2021-05-10', 'merchant_code': 'tim_hortons', 'amount_cents': 1321}
    }

    test_transactions3 = {
        'T1': {'date': '2021-05-09', 'merchant_code': 'sportcheck', 'amount_cents': 2500},
        'T2': {'date': '2021-05-10', 'merchant_code': 'tim_hortons', 'amount_cents': 1000},
        'T3': {'date': '2021-05-10', 'merchant_code' : 'the_bay', 'amount_cents': 500}
    }

    max_reward1, transaction_map1 = calculate_rewards(test_transactions1)
    max_reward2, transaction_map2 = calculate_rewards(test_transactions2)
    max_reward3, transaction_map3 = calculate_rewards(test_transactions3)

    st.write("""
    # Capital One Assessment 
    """)

    transaction_test_df_1 = pd.DataFrame.from_dict(test_transactions1, orient='index')
    transaction_test_df_1 = transaction_test_df_1.rename(
        columns={'date': 'transaction_date', 'merchant_code': 'merchant', 'amount_cents': 'amount'})

    transaction_test_df_2 = pd.DataFrame.from_dict(test_transactions2, orient='index')
    transaction_test_df_2 = transaction_test_df_2.rename(
        columns={'date': 'transaction_date', 'merchant_code': 'merchant', 'amount_cents': 'amount'})

    transaction_test_df_3 = pd.DataFrame.from_dict(test_transactions3, orient='index')
    transaction_test_df_3 = transaction_test_df_3.rename(
        columns={'date': 'transaction_date', 'merchant_code': 'merchant', 'amount_cents': 'amount'})

    df1 = pd.DataFrame.from_dict(transaction_map1, orient='index', columns=['reward points'])
    df2 = pd.DataFrame.from_dict(transaction_map2, orient='index', columns=['reward points'])
    df3 = pd.DataFrame.from_dict(transaction_map2, orient='index', columns=['reward points'])

    with st.container():
        col1, col2 = st.columns(2, gap="medium")
        with col1:
            st.dataframe(transaction_test_df_1)
        with col2:
            st.dataframe(df1)
            st.metric(f"Max reward points", max_reward1)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(transaction_test_df_2)
        with col2:
            st.dataframe(df2)
            st.metric(f"Max reward points", max_reward2)

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.dataframe(transaction_test_df_3)
        with col2:
            st.dataframe(df3)
            st.metric(f"Max reward points", max_reward3)
