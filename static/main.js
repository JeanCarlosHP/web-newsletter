const date = document.querySelector('header>p>span')
const content = document.querySelector('#content')

getData()

async function getData() {
  const response = await fetch('http://127.0.0.1:8000/json')
  const responseJson = await response.json()

  localStorage.setItem('data', JSON.stringify(responseJson))
  const contentJson = JSON.parse(localStorage.getItem('data'))

  date.innerHTML += contentJson.date
  content.innerHTML += contentJson.content
}
