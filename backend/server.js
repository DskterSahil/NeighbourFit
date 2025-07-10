const express = require('express')
const cors = require('cors')
const fs = require('fs')
const app = express()
const port = 3000

app.use(cors())
app.use(express.json())

const neighborhoodsData = JSON.parse(fs.readFileSync('processed_delhi_data.json'))

app.post('/match', (req, res) =>{
    const userWeights = req.body // More descriptive name

    // This map connects frontend keys to JSON keys
    const keyMap = {
        metro_dist : 'norm_nearestetro',
        friendly_neigh : 'norm_family_friendly',
        cafe_restaurants : 'norm_cafe',
        studentPref : 'norm_student_friendly',
        community : 'norm_community',
        hospitals : 'norm_hospital'
    }

    const scoredNeighborhoods = neighborhoodsData.map( hood => { // More descriptive name
        let totalScore = 0
        let totalWeight = 0 // Will be a number

        for(const metric in userWeights){
            const normKey = keyMap[metric]
            
            if(hood.hasOwnProperty(normKey) && userWeights[metric]){
                const normScore = hood[normKey]
                // ❗ CRITICAL FIX: Convert the incoming user weight from a string to a number
                const userWeight = parseInt(userWeights[metric], 10)

                totalScore += normScore * userWeight
                totalWeight += userWeight // Now this is a proper mathematical addition
            }
        }

        const finalScore = (totalWeight > 0) ? (totalScore / totalWeight) : 0

        return {
            name : hood.name,
            score : finalScore * 100
        }
    })

    scoredNeighborhoods.sort((a,b) => b.score - a.score)
    res.json(scoredNeighborhoods)
})

app.get('/', (req, res) =>{
    res.send("Backend is up and running!!")
})

app.listen(port, ()=> {
    console.log(`🚀 Server running on http://localhost:${port}`)
})