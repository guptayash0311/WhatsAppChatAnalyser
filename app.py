import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("WhatsApp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)
    
    st.dataframe(df)
    
    # Fetch Unique Users
    user_list = df['users'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show Analysis w.r.t.",user_list)
    
    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.subheader("Total Msgs")
            st.subheader(num_messages)
        with col2:
            st.subheader("Total Words")
            st.subheader(words)
        with col3:
            st.subheader("Media Shared")
            st.subheader(num_media_messages)
        with col4:
            st.subheader("Links Shared")
            st.subheader(num_links)
        
        # Finding most busy users in the group(Only Group Level)
        if selected_user == 'Overall':
            st.title("Most Busy Users:")
            x, new_df = helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1, col2 = st.columns(2)

            with col1:
                ax.bar(x.index,x.values,color='brown')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)
                
        # Wordcloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user,df)
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)
        
        # Most Common Words
        most_common_df=helper.most_common_words(selected_user,df)
        fig, ax = plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)
        
            