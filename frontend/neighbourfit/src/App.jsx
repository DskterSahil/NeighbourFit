import React from 'react'
import axios from 'axios'
import './App.css'

export default function App(){
  const [preference, setPreference] = React.useState({
    'metro_dist' : 3,
    'friendly_neigh' : 3,
    'cafe_restaurants' : 3,
    'isStudent' : "False",
    'studentPref' : 3,
    'community' : 3,
    'hospitals' : 3,
  })

  const [results, setResults] = React.useState([])
  const [loading, setLoading] = React.useState(false)


  function updateVal(event){
    setPreference(prevPref => ({
      ...prevPref,
      [event.target.name] : event.target.value
    }))
  }

  async function handleSubmit(event){
    event.preventDefault()
    setLoading(true)
    const parameters = {...preference}

    if(parameters.isStudent == "False"){
        delete parameters.studentPref
    }
    delete parameters.isStudent

    try{
      const response = await axios.post("https://neighborfit-api-ly4c.onrender.com/match", parameters);
      setResults(response.data)
    }
    catch(err){
      console.error("Error while fetching....", err)

    }
    setLoading(false)
  }




  return (
    <>
      <h1>NeighbourFit</h1>

      <form onSubmit={handleSubmit} >

       <p>Are you a student?</p>
      <label htmlFor="student-yes">
        <input
          type="radio"
          name="isStudent"
          value="True"
          id="student-yes"
          onChange={updateVal}
          checked={preference.isStudent === "True"}
        />
        Yes
      </label>

      <label htmlFor="student-no" style={{ marginLeft: "10px" }}>
        <input
          type="radio"
          name="isStudent"
          value="False"
          id="student-no"
          onChange={updateVal}
          checked={preference.isStudent === "False"}
        />
        No
      </label>

      <label htmlFor="metro_dist">Metro Proximity:- {preference.metro_dist}</label>
      <input 
      type="range" 
      name="metro_dist" 
      id="metro_dist"  
      min="1" 
      max="5" 
      value={preference.metro_dist}  
      onChange={updateVal} 
      />

      <label htmlFor="community_norm">Community Feel:- {preference.community}</label>
      <input 
      type="range" 
      name="community" 
      id="community_norm"  
      min="1" 
      max="5" 
      value={preference.community} 
      onChange={updateVal}
        />

      <label htmlFor="friendlyness">Family Friendly:- {preference.friendly_neigh} </label>
      <input 
      type="range" 
      name="friendly_neigh" 
      id="friendlyness"  
      min="1" 
      max="5" 
      value={preference.friendly_neigh} 
      onChange={updateVal} 
       />

       {preference.isStudent == "True" && (
        <>
         <label htmlFor="study">Study & Coaching:- {preference.studentPref} </label>
         <input 
         type="range" 
         name="studentPref" 
         id="study"  
         min="1" 
         max="5" 
         value={preference.studentPref} 
         onChange={updateVal} 
          />
          </>
       )}



      <button>{loading ? 'Finding...' : 'Find My Neighbourhood'} </button>
        

      </form>

       {loading === false && (

        <div className='results-container'>
          {results.map(item => (
            <div key={item.name}>
              <h3>{item.name}</h3>
              <p> {Math.round(item.score)}% Match</p>
            </div>
          ))}
        </div>
       )}
    </>
  )
}