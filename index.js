import React from 'react'
import { useState } from 'react'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faArrowLeft, faArrowRight } from '@fortawesome/free-solid-svg-icons';



function Home() {
  const [subreddit, setSubreddit] = useState('reddit.com')
  const [activeTab, setActiveTab] = useState({month: false, week: false, day: true});
  const [postsDay, setPostsDay] = useState(0)
  const [postsWeek, setPostsWeek] = useState(0)
  const [postsDayTotal, setPostsDayTotal] = useState([[]])
  const [postsWeekTotal, setPostsWeekTotal] = useState([[]])
  const [postsMonth, setPostsMonth] = useState([]) 
  
  const handleDayChangeBtn = (event) => {
    const cur_day = postsDay + parseInt(event.target.value)
    console.log('curday:', cur_day)
    if (cur_day > postsDayTotal.length - 1) {
      handleNextMonthChange(event)
    } else if (cur_day < 0) {
      const month = parseInt(document.getElementById('monthSelect').value)
      const year = parseInt(document.getElementById('yearSelect').value)
      const date = new Date(year, month +1 , 0).getDate()
      handleNextMonthChange(event)
      //date - 1 is correct here but it is either too fast or maybe the state hasnt changed yet...idk
      //have it set to -2 for now so it wont break unless you go back into febuary
      console.log(date-1)
      setPostsDay(date - 2)
    } else {
      setPostsDay(cur_day)
    }
  }

  const handleNextWeekBtn = (event) => {
    const cur_week = postsWeek + parseInt(event.target.value)
    if (cur_week > 3) {
      handleNextMonthChange(event)
    } else if (cur_week < 0) {
      handleNextMonthChange(event)
      setPostsWeek(3)
    }else {
      setPostsWeek(postsWeek + parseInt(event.target.value))
    }
  }

  const handleNextMonthChange =  (event) => {
    console.log(event.target.value)
    const nextMonth = parseInt(document.getElementById('monthSelect').value) + parseInt(event.target.value)
    if(nextMonth == 13){
      document.getElementById('monthSelect').value = '01'
      handleNextYearChange(event)
    } else if (nextMonth == 0){
      document.getElementById('monthSelect').value = '12'
      handleNextYearChange(event)
    } else {
      document.getElementById('monthSelect').value = nextMonth.toString().padStart(2, '0')
    }
    console.log('Month =',document.getElementById('monthSelect').value)
    fetchPosts()
  }

  const handleNextYearChange = (event) => {
    const nextYear = parseInt(document.getElementById('yearSelect').value) + parseInt(event.target.value)
    document.getElementById('yearSelect').value = nextYear.toString().padStart(4, '0')
  }

  const handleSubredditChange = (event) => {
    setSubreddit(event.target.value)
  }

  const handleSubmit = (event) => {
    event.preventDefault();
    setActiveTab({month: true, week: false, day: false}) 
    fetchPosts()
  }
    
  const fetchPosts = async () => { 
    setPostsDay(0)
    setPostsWeek(0)

    const range = document.getElementById('monthSelect').value == 13 ? 'year' : 'month'
    const requestBody = {
      month: document.getElementById('monthSelect').value,
      year: document.getElementById('yearSelect').value,
      subreddit: subreddit,
      range: range
    };

    const response = await fetch('http://127.0.0.1:5000/form', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(requestBody),
    });
  
    const data = await response.json()
    setPostsMonth(data.month.length > 0 ? data.month[0] : [])
    setPostsDayTotal(data.month.length > 0 ? data.days : [])
    setPostsWeekTotal(data.month.length > 0 ? data.weeks : [])
    console.log(data)
  }


return (

  <div className='p-5 flex flex-col items-center gap-y-5 bg-zinc-950 text-zinc-200 min-h-screen'>
  <div>
    <h1 className='text-5xl text-center font-bold	'> Best of Reddit </h1>
    <h2 className='text-base text-center'> Find the top posts you missed months ago </h2>
  </div>
  <form id='form' onSubmit={handleSubmit} className='text-center w-5/12 flex flex-row justify-between'>
    <div className='bg-zinc-950'>
      <label> Month: </label>
      <select className='bg-zinc-200 hover:outline rounded-3xl text-zinc-900 pr-1 pl-1' defaultValue={'11'} id="monthSelect">
        <option value={'01'}>January</option>
        <option value={'02'}>February</option>
        <option value={'03'}>March</option>
        <option value={'04'}>April</option>
        <option value={'05'}>May</option>
        <option value={'06'}>June</option>
        <option value={'07'}>July</option>
        <option value={'08'}>August</option>
        <option value={'09'}>September</option>
        <option value={'10'}>October</option>
        <option value={'11'}>November</option>
        <option value={'12'}>December</option>
        <option value={'13'}> Entire year </option>
      </select>
    
      <label> Year: </label>
      <select className='bg-zinc-200 hover:outline rounded-3xl text-zinc-900 pr-1 pl-1' defaultValue={'2005'} id='yearSelect'>
        <option value={'2005'}>2005</option>
        <option value={'2006'}>2006</option>
        <option value={'2007'}>2007</option>
        <option value={'2008'}>2008</option>
        <option value={'2009'}>2009</option>
        <option value={'2010'}>2010</option>
        <option value={'2011'}>2011</option>
        <option value={'2012'}>2012</option>
        <option value={'2013'}>2013</option>
        <option value={'2014'}>2014</option>
        <option value={'2015'}>2015</option>
        <option value={'2016'}>2016</option>
        <option value={'2017'}>2017</option>
        <option value={'2018'}>2018</option>
        <option value={'2019'}>2019</option>
        <option value={'2020'}>2020</option>
        <option value={'2021'}>2021</option>
        <option value={'2022'}>2022</option>
        <option value={'2023'}>2023</option>
      </select>
    </div>
    
    <div>
      <label> Subreddit: </label>
      <input className='bg-zinc-200 text-zinc-900 rounded-full text-center w-1/2 ml-2' type="text" value={subreddit} onChange={handleSubredditChange} id="subreddit" name="subreddit" />
    </div>

    <button className='bg-zinc-200 rounded-full px-4 boarder border-zinc-900 text-zinc-900' id='submit' type="submit">Submit</button>
  </form>

  <div className="gap-4 flex justify-around w-6/12 bg-zinc-950">
    <div>
    {activeTab.day && <button className='active:bg-gray-600 hover:italic' value={-1} onClick={handleDayChangeBtn}> <FontAwesomeIcon className='pointer-events-none hover:outline' icon={faArrowLeft}/> Previous Day </button> }
    {activeTab.week && <button className='active:bg-gray-600 hover:italic' id='nextWeek' value={-1} type='button' onClick={handleNextWeekBtn}> <FontAwesomeIcon className='pointer-events-none' icon={faArrowLeft}/> Previous Week </button>} 
    {activeTab.month && <button className='active:bg-gray-600 hover:italic' value={-1} onClick={handleNextMonthChange}> <FontAwesomeIcon className='pointer-events-none' icon={faArrowLeft}/> Previous Month </button>}
    </div>
    <div className="gap-4 flex">
    <div>|</div>
    <button className='active:bg-gray-600 hover:underline' onClick={() => setActiveTab({month: false, week: false, day: true})}> View by day </button>
    <div>|</div>
    <button className='active:bg-gray-600 hover:underline' onClick={() => setActiveTab({month: false, week: true, day: false})}> View by Week </button>
    <div>|</div>
    <button className='active:bg-gray-600 hover:underline' onClick={() => setActiveTab({month: true, week: false, day: false})}> View by Month </button>
    <div>|</div>
    </div>
    <div>
    {activeTab.month && <button className='active:bg-gray-600 hover:italic' value={1} onClick={handleNextMonthChange}> Next Month <FontAwesomeIcon className='pointer-events-none'  icon={faArrowRight}/> </button>}
    {activeTab.week && <button className='active:bg-gray-600 hover:italic' id='nextWeek' value={1} type='button' onClick={handleNextWeekBtn}> Next Week <FontAwesomeIcon className='pointer-events-none'  icon={faArrowRight}/>  </button>} 
    {activeTab.day && <button className='active:bg-gray-600 hover:italic' value={1} onClick={handleDayChangeBtn}> Next Day <FontAwesomeIcon className='pointer-events-none'  icon={faArrowRight}/> </button>} 
    </div>
  </div>


  <div className='grid grid-cols-3 w-6/12 gap-5'> 
    {activeTab.month === true && postsMonth.map((post, index) => { 
      return (
        <div key={index} className='border rounded border-slate-700 h-28 flex flex-col justify-between p-1 bg-zinc-900 hover:bg-zinc-800'>
          <a className='h-2/4 line-clamp-2 overflow-hidden' href={'https://www.reddit.com/r/reddit.com/comments/'+post.id} target="_blank" rel="noopener noreferrer">{post.title}</a>
          <div className='text-center self-bottom'> Upvotes: {post.score} </div>
        </div>
      )
    })}

    {activeTab.week === true && postsWeekTotal[postsWeek].map((post, index) => {
          return (
            <div key={index} className='border rounded border-slate-700 h-28 flex flex-col justify-between p-1 bg-zinc-900 hover:bg-zinc-800'> 
              <a href={'https://www.reddit.com/r/reddit.com/comments/'+post.id} target="_blank" rel="noopener noreferrer"> {post.title} </a>
              <div className='text-center self-bottom'> Upvotes: {post.score} </div>
            </div>
          )
        })}

    {activeTab.day === true && postsDayTotal[postsDay].map((post, index) => {
        return (
          <div key={index} className='border rounded border-slate-700 h-28 flex flex-col justify-between p-1 bg-zinc-900 hover:bg-zinc-800'> 
            <a href={'https://www.reddit.com/r/reddit.com/comments/'+post.id} target="_blank" rel="noopener noreferrer">{post.title}</a>
            <div className='text-center self-bottom'> Upvotes: {post.score} </div>
          </div>
        )
      })}
  </div>

  </div>
)

}

export default Home

