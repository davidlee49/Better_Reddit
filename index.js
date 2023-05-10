import React from 'react'
import Link from 'next/link'
import { useState } from 'react'


// export async function getStaticProps() {
//   const response = await fetch(`http://127.0.0.1:5000/members`)
//   const data = await response.json()

//   console.log(data)
//   return {
//       props: {
//           posts: data
//       }
//   }
// }


function Home() {
  const [posts, setPosts] = useState([])
  const [selectedDateStart, setSelectedDateStart] = useState('2005-08-08'); 
  const [selectedDateEnd, setSelectedDateEnd] = useState('2005-09-09'); 

  const handleStartDateChange = (event) => {
    setSelectedDateStart(event.target.value);
  };

  const handleEndDateChange = (event) => {
    setSelectedDateEnd(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    const formData = new FormData(event.target);

    const response = await fetch('http://127.0.0.1:5000/form', {
      method: 'POST',
      body: formData,
    });
  
    const data = await response.json();
  
    setPosts(data.posts)
  }
  

  return (

    <>
    <button><Link href={'/search'}> Test </Link></button>
    <h1> Better Reddit </h1>
    <h2> Find what what you saw a month ago </h2>
    <div>asdf</div>

    <form action="http://127.0.0.1:5000/form" method="post" onSubmit={handleSubmit} >
      <label for="created_utc_start"> Date range start </label>
      <input type="date" value={selectedDateStart} onChange={handleStartDateChange} id="created_utc_start" name="created_utc_start" />

      <label for="created_utc_end"> Date range end </label>
      <input type="date" value={selectedDateEnd} onChange={handleEndDateChange} id="created_utc_end" name="created_utc_end" />

      <label for="subreddit"> Subreddit: </label>
      <input type="text" id="subreddit" name="subreddit" />

      <label for="title"> Title </label>
      <input type="text" id="title" name="title" />

      

{/* 
      <label for="author"> Reddit user:</label>
      <input type="text" id="author" name="author" />

      <label for="clicked"> Have you seen it? </label>
      <input type="text" id="clicked" name="clicked" />
      
      <label for="comments"> Comments </label>
      <input type="text" id="comments" name="comments" />

      <label for="distinguished"> Was it distinguished? </label>
      <input type="text" id="distinguished" name="distinguished" />
      
      <label for="edited"> Was it edited </label>
      <input type="text" id="edited" name="edited" />
      
      <label for="id"> ID </label>
      <input type="text" id="id" name="id" />
      
      <label for="is_original_content"> Was it original content? </label>
      <input type="text" id="is_original_content" name="is_original_content" />
      
      <label for="is_self"> Self post? </label>
      <input type="text" id="is_self" name="is_self" />
      
      <label for="locked"> Locked? </label>
      <input type="text" id="locked" name="locked" />
      
      <label for="name"> Name </label>
      <input type="text" id="name" name="name" />
      
      <label for="num_comments"> Number of comments? </label>
      <input type="text" id="num_comments" name="num_comments" />
      
      <label for="over_18"> NSFW </label>
      <input type="text" id="over_18" name="over_18" />
      
      <label for="permalink"> Permalink </label>
      <input type="text" id="permalink" name="permalink" />
      
      <label for="poll_data"> Poll? </label>
      <input type="text" id="poll_data" name="poll_data" />
      
      <label for="saved"> Saved? </label>
      <input type="text" id="saved" name="saved" />
      
      <label for="score"> Upvotes? </label>
      <input type="text" id="score" name="score" />
      
      <label for="selftext"> Self Text </label>
      <input type="text" id="selftext" name="selftext" />

      <label for="spoiler"> Spoiler </label>
      <input type="text" id="spoiler" name="spoiler" />
      
      <label for="stickied"> Stickied? </label>
      <input type="text" id="stickied" name="stickied" />
      
      <label for="upvote_ratio"> Upvote ratio </label>
      <input type="text" id="upvote_ratio" name="upvote_ratio" />

      <label for="url"> URL </label>
      <input type="text" id="url" name="url" />
      */}

      <button type="submit">Submit</button>

    </form>

 
    {posts.map((post) => {
      return (
        <div> 
          <a href={post[2].url}> {post[2].url} </a>
          {/* <img src={post[2]} /> */}
        </div>
      )
      
    })}
    </>
  )
}

export default Home
