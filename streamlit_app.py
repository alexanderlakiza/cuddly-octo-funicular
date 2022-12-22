import streamlit as st

from course_work.my_rec_sys.recsys import check_movie_appearance, RecommendationSystem


@st.cache(ttl=100000)
def get_recs(movies):
    rec_sys = RecommendationSystem()
    return rec_sys.get_recs(movies)


st.title("Рекомендательная система")
st.markdown("## Как устроена рекомендательная система")
st.markdown("Введите один, два или три фильма в "
            "поля ниже. К сожалению, база фильмов небольшая - всего 4.8 тысячи фильмов "
            "(В основном, фильмы 21 века, выпущенные до начала 2017 года). "
            "Названия фильмов необходимо вводить по-английски. Если вы не знаете название фильма по-английски, то"
            " вы можете найти свой фильм на [Кинопоиске](https://www.kinopoisk.ru) и взять английское название "
            "фильма оттуда (они находятся под российскими названиями фильмов). Или вы можете посмотреть в "
            "[эксель "
            "таблице](https://docs.google.com/spreadsheets/d"
            "/1o939ac04UdB6rcXJH6eB0htRyzBi6icnAlkt2WoumOk/edit?usp=sharing), какие фильмы есть в базе. "
            "После того, как вы введёте названия фильмов, необходимо нажать на кнопку, и тогда сервис предложит "
            "вам 10 фильмов, которые больше всего похожи на те, что вы указали")

with st.form("Watched Movies"):
    st.write("Введите от 1 до 3 своих любимых фильма")
    movie1 = st.text_input("Первый фильм")
    movie2 = st.text_input("Второй фильм")
    movie3 = st.text_input("Третий фильм")

    # Every form must have a submit button.
    submitted = st.form_submit_button("Узнать рекомендации")

    st.write('Попробуйте, например, ввести: The Avengers, Spectre, Toy Story 3')

if submitted:
    movies = [movie1, movie2, movie3]
    for movie in movies:
        if movie and not check_movie_appearance(movie1):
            st.error(f'Фильм "__{movie}__" не был найден в нашей базе. Пожалуйста, убедитесь, что вы '
                     f'правильно ввели английское название фильма. Если вы уверены, что ввели его правильно, '
                     f'значит фильма нет в нашей базе, выберите другой фильм или оставьте поле пустым')
            break
    else:
        st.markdown("---")
        st.markdown("## Рекомендации")
        recs_10 = get_recs(movies)
        for rec_movie in recs_10:
            st.success(f'Вам следует посмотреть __"{rec_movie}"__')
