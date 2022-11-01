let imgBase46;
let movie_data;
downloadImg = () => {
  let a = document.getElementById('downloadImg')
  a.href = imgBase46
  a.download = `${movie_data.name}.png`; //File name
  a.click(); //Downloaded file
}

editMovie = () => {
  document.getElementsByName('editTitle')[0].value= movie_data.name;
  document.getElementsByName('currentName')[0].value = movie_data.name;
  document.getElementsByName('editOverview')[0].value = movie_data.overview;
}


deleteMovie = () => {
      fetch('/deletemovie', {
    method: 'POST', 
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(movie_data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log('Success:', data);
    })
    .catch((error) => {
      console.error('Error:', error);
    });
    document.getElementById('successAlert').innerHTML= `Film : ${movie_data.name} has been deleted.`;
    document.getElementById('successAlert').style.display='block';
    document.getElementById('movieCard').style.display='none';
}

async function getPoster() {
  let search_query = document.getElementById("queryMovie").value;
  let search_url = `/poster/${search_query}`
  let img_src_res;
  const res = await fetch(`${search_url}`)
  response = await res.json();
  movie_data = response
  console.log(img_src_res)
  img_src_res = response.image
  let img_src = `data:image/png;base64, ${img_src_res}`
  imgBase46 = img_src
  document.getElementById("posterImg").src = img_src;
  document.getElementById("movieTitle").innerHTML = response.name
  document.getElementById("movieRating").innerHTML = response.rating
  document.getElementById("movieOverview").innerHTML = response.overview
  document.getElementById("releaseDate").innerHTML = response.release
  document.getElementById('posterDiv').style.display='block';
  document.getElementById('successAlert').style.display='none';
  document.getElementById('movieCard').style.display='block';
  editMovie();
}