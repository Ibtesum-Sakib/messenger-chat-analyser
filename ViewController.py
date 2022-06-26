from __future__ import division
import streamlit as st

import json
from streamlit_lottie import st_lottie

import matplotlib.pyplot as plt
import preprocessor, helper
import seaborn as sns
from ui_components import download_button
from ui_components import load_lottieurl
#import nltk
#nltk.download('vader_lexicon')
#from nltk.sentiment.vader import SentimentIntensityAnalyzer
#sentiment_analyzer = SentimentIntensityAnalyzer()

import base64


class ViewController:
    def __init__(self):

        st.set_page_config(
            page_title='Messenger Chat Analyser',
            page_icon=':test_tube:',
            layout='centered',
            initial_sidebar_state='auto',

        )
        self.lottie_chat = load_lottieurl('phone_chat.json')
        self.lottie_message = load_lottieurl('chatting.json')
        self.github_link = 'https://github.com/Ibtesum-Sakib/messenger-chat-analyser'
        self.file_path = 'message.json'
        self.lottie_data = load_lottieurl('data_analysis_animation.json')

    def build_graph_ui(self):
        c1, c2 = st.columns((2, 1))
        c1.title("""Messenger Chat Analyser""")
        c1.subheader("""Discover trends, analyse your chat history and judge your friends!""")
        c1.markdown(
            f"Don't worry, we're not interested in peeking, we are not about that; in fact, you can check the code in here: [link]({self.github_link})")
        uploaded_file = c1.file_uploader(label="""Upload your Mesenger chat here in "JSON" file-format, don't worry, we won't peek""")

        with open(self.file_path, 'r') as f:
            dl_button = download_button(f.read(), 'sample_file.json', 'Try it out with my sample file!')
            c1.markdown(dl_button, unsafe_allow_html=True)

        with c2:
            st_lottie(self.lottie_chat, speed=1, height=400, key="msg_lottie")
        if uploaded_file is not None:
            data = json.load(uploaded_file)
            df = preprocessor.preprocess(data)

            # fetching unique user
            sender_list = df['sender_name'].unique().tolist()
            sender_list.sort()
            sender_list.insert(0, "Overall")

            st.subheader("Chat Members")
            st.subheader(f" Your file has **{len(sender_list[1:])}** members.")

            selected_sender = st.selectbox("Show analysis with respect to Overall or your preference", sender_list)

            if st.button("Show Analysis"):

                num_messages, words, num_of_media, num_of_call = helper.fetch_stats(selected_sender, df)

                # number of columns
                st.title('Top Analysis')
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.subheader("Total Messages")
                    st.subheader(num_messages)

                with col2:
                    st.subheader("Total Words")
                    st.subheader(words)

                with col3:
                    st.subheader("Links Shared")
                    st.subheader(num_of_media)

                with col4:
                    st.subheader("Total Calls")
                    st.subheader(num_of_call)

                # monthly_timeline
                st.header("Monthly Timeline")
                st.subheader("When did you have the most conversations in a month?")
                st.markdown(
                    f"This basically shows how much effort each person puts into each message; the more words per message, the more it appears that the person is making a real effort.")
                timeline = helper.monthly_timeline(selected_sender, df)
                fig, ax = plt.subplots()
                ax.plot(timeline['time'], timeline['content'], color='indigo')
                plt.title("Monthly Timeline", loc = 'left')
                plt.xlabel("Month")
                plt.ylabel("Messages Per Month")
                plt.xticks(rotation= 30)
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.xaxis.label.set_color('darkblue')  # setting up X-axis label color to yellow
                ax.yaxis.label.set_color('crimson')
                st.pyplot(fig)

                # daily_timeline
                st.subheader("Daily Timeline")
                st.subheader("How often do you talk?")
                st.markdown(
                    f"This demonstrates the times of day when you two converse the most! To see how your friends' choices have evolved over time, alter your friend selection.")
                daily_timeline = helper.daily_timeline(selected_sender, df)
                fig, ax = plt.subplots()
                ax.plot(daily_timeline['date_only'], daily_timeline['content'], color='darkblue')
                plt.xticks(rotation= 30)
                plt.xlabel("Date")
                plt.ylabel("Messages Per Day")
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.xaxis.label.set_color('darkblue')  # setting up X-axis label color to yellow
                ax.yaxis.label.set_color('crimson')
                st.pyplot(fig)

                # Activity map
                st.subheader("Activity of the members")
                col1, col2 = st.columns(2)

                with col1:
                    st.header("Most Busy Day")
                    st.subheader("Who sends the bigger messages?")
                    st.markdown(
                        f"This one shows the average message length, apparently **{helper.most_wpm_winner(selected_sender, df)}** puts the most effort for each message")
                    busy_day = helper.week_activity_map(selected_sender, df)
                    fig, ax = plt.subplots()
                    rects1 = ax.bar(busy_day.index, busy_day.values, color='crimson')
                    plt.xlabel("Name of the day")
                    plt.ylabel("Messages Per Day")
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.xaxis.label.set_color('darkblue')  # setting up X-axis label color to yellow
                    ax.yaxis.label.set_color('Crimson')
                    plt.xticks(rotation=30)

                    def autolabel(rects):
                        # attach some text labels
                        for rect in rects:
                            height = rect.get_height()
                            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                                    '%d' % int(height),
                                    ha='center', va='bottom')

                    autolabel(rects1)

                    st.pyplot(fig)

                with col2:
                    st.header("Most Busy Month")
                    st.subheader("How long do your conversations last?")
                    st.markdown(
                        f"This is how many messages (on average) your conversations had; the more of them there are, the more messages you guys exchanged every time one of you started the conversation!")
                    busy_month = helper.month_activity_map(selected_sender, df)
                    fig, ax = plt.subplots()
                    rects1 = ax.bar(busy_month.index, busy_month.values, color='orange')
                    plt.xticks(rotation=30)
                    plt.xlabel("Name of the month")
                    plt.ylabel("Messages Per month")
                    ax.spines['top'].set_visible(False)
                    ax.spines['right'].set_visible(False)
                    ax.xaxis.label.set_color('darkblue')  # setting up X-axis label color to yellow
                    ax.yaxis.label.set_color('Crimson')

                    def autolabel(rects):
                        # attach some text labels
                        for rect in rects:
                            height = rect.get_height()
                            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                                    '%d' % int(height),
                                    ha='center', va='bottom')

                    autolabel(rects1)

                    st.pyplot(fig)

                st.header("Weekly activity map")
                st.subheader("When were you and your friends the most active in a week?")
                st.markdown(
                    f"This is how many messages each one of you have exchanged per **week** and most messages on **{helper.max_msg_d(selected_sender, df)}**, the most messages you guys have exchanged in a week was **{helper.max_msg_c(selected_sender, df)}** on the time period of **{helper.max_timeop(selected_sender, df)}**")
                user_heatmap = helper.activity_heatmap(selected_sender, df)
                plt.figure(figsize=(20, 6))
                fig, ax = plt.subplots()
                ax = sns.heatmap(user_heatmap)
                st.pyplot(fig)

                # Finding the busiest user
                if selected_sender == 'Overall':
                    st.header('Most Busy Users')
                    x, new_df = helper.most_busy_users(df)
                    fig, ax = plt.subplots()

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        col1.subheader("Who takes the longest message reply?")
                        col1.markdown(f" **{helper.most_messages_winner(selected_sender, df)}** won this one and sends total **{helper.most_msg_by_busy_user(df)}** messages")
                        rects1 = ax.bar(x.index, x.values, color=['darkblue', 'yellow','indigo','black','green'])
                        plt.xlabel("Name of the busiest user")
                        plt.ylabel("Amount of Messages")
                        ax.spines['top'].set_visible(False)
                        ax.spines['right'].set_visible(False)
                        ax.xaxis.label.set_color('darkblue')  # setting up X-axis label color to yellow
                        ax.yaxis.label.set_color('crimson')
                        plt.xticks(rotation= 30)

                        def autolabel(rects):
                            # attach some text labels
                            for rect in rects:
                                height = rect.get_height()
                                ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                                        '%d' % int(height),
                                        ha='center', va='bottom')

                        autolabel(rects1)

                        st.pyplot(fig)

                    with col2:
                        col2.subheader("Who talks the most?")
                        col2.markdown(
                            f"How many messages has each one sent in your convo? apparently **{helper.most_messages_winner(selected_sender, df)}** did")
                        st.dataframe(new_df)

                    with col3:
                        col3.subheader("Who's starts the conversations?")
                        col3.markdown(
                            f"This clearly shows that **{helper.most_messages_winner(selected_sender, df)}** started almost all the convos")
                        fig, ax = plt.subplots()
                        ax.pie(x.values, labels=x.index, autopct="%.2f")
                        st.pyplot(fig)

#most common word
                st.subheader('Most Common Words')
                st.subheader(f"This basically shows the top 20 words in your conversation.")

                most_common_df = helper.most_common_words(selected_sender, df)

                fig, ax = plt.subplots()

                ax.barh(most_common_df['word'], most_common_df['count'], color='indigo')
                plt.xlabel("Number of words")
                plt.ylabel("Most common words")
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.xaxis.label.set_color('darkblue')  # setting up X-axis label color to yellow
                ax.yaxis.label.set_color('crimson')
                # plt.xticks(rotation='vertical')
                st.pyplot(fig)
                # st.dataframe(most_common_df)

                # Emoji analysis
               # emoji_df = helper.emoji_helper(selected_sender, df)
               # st.subheader("Emoji Analysis")
               # st.dataframe(emoji_df)

                #sentiment
                st.title("Sentiment of members")
                st.subheader("Who was the most positive in your convo?")
                st.markdown(
                    f" Apparently **{helper.max_positivity(selected_sender, df)}** was! The positivity is **{helper.sn_num(selected_sender, df)}** percent")
                sentiment_of_user = helper.sentiment_analysis(selected_sender, df)
                #st.text(sentiment_of_user)
                plt.figure(figsize=(20, 10))
                fig, ax = plt.subplots()
                ax.plot(sentiment_of_user, 'g-o', markerfacecolor='lightgreen')
                ax.plot(sentiment_of_user, 'r-s', markerfacecolor='lightblue')
                plt.xticks(rotation=30)
                plt.xlabel("Number of Month")
                plt.ylabel("Sentiment")
                ax.spines['top'].set_visible(False)
                ax.spines['right'].set_visible(False)
                ax.xaxis.label.set_color('darkblue')  # setting up X-axis label color to yellow
                ax.yaxis.label.set_color('crimson')


                st.pyplot(fig)



        thanks_line = """Special thanks to jrieke for making the custom CSS download button and akiragondo for the design idea!"""
        st.markdown("""    <style>
        footer {
            visibility: hidden;
            }
        footer:after {
            content:'""" + thanks_line + """'; 
            visibility: visible;
            display: block;
            position: relative;
            #background-color: red;
            padding: 5px;
            top: 2px;
        }</style>""", unsafe_allow_html=True)

    def build_about_me_ui(self):
        st.title("About the Creator")
        c1, c2 = st.columns([1, 1])
        c1.markdown(
            "Hey! My name is Mohammad Ibtesum Sakib, a Computer Science Engineer from Bangladesh! This page is still under "
            "construction since I want to finish the rest of the app before I focus on this bit, but if you "
            "would like to ask me anything of if you have any projects you think I could be a good addition "
            "to, please, send me a message at ibtesum38@gmail.com \n"
        "\nYou can also visit https://ibtesum-sakib.github.io/")
        c2.image('me.jpg')

    def build_conversation_explanation(self):
        st.title('How does the chat analyser work?')
        c1, c2 = st.columns([1, 1])
        c1.header('Data Analysis')
        c1.markdown("""The foundation of this app is made up of very basic data analysis, like adding up the times of day that messages were sent or counting the number of messages sent each month. However, calculations like the longest time in messages and sentiment of the conversation aren't so simple, so we'll go deeper right now!""")
        with c2:
            st_lottie(self.lottie_data, height=300)
        st.header('Conversations')
        st.markdown("""In order to analyse conversations, we need to first find a way to define conversations based 
        on a sequence of individual messages. To do that, let's make our definition of a conversation:""")
        st.info("""Conversations:        
        The event of the exchange of messages between two people during a certain period of time""")
        st.header('Sentiment Analysis')
        st.info("""Sentiment Analysis:        
                Sentiment analysis examines the subjective content of a statement, such as opinions, assessments, emotions, or attitudes toward a subject, person, or object. Positive, negative, or neutral expressions can all be categorized. For instance, say, "I really like the new design of your website!" is positve""")


    def build_sidebar(self):

        with st.sidebar:
            st_lottie(self.lottie_message, quality='High', height=120, key='message_lottie')
        st.sidebar.title("Messenger Chat Analyser")
        pages = [
            'Messenger Chat Analyser',
            'How does the Chat Analyser Work?',
            'About the Creator'
        ]
        selected_page = st.sidebar.radio(
            label='Page',
            options=pages
        )
        return selected_page

    def build_ui(self):
        selected_page = self.build_sidebar()
        if selected_page == 'Messenger Chat Analyser':
            self.build_graph_ui()
        elif selected_page == 'How does the Chat Analyser Work?':
            self.build_conversation_explanation()
        elif selected_page == 'About the Creator':
            self.build_about_me_ui()
