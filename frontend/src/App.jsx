import axios from "axios"

function App() {
  const handleSumbit = async (e) => {
    e.preventDefault()
    let data = {
      "BMI": 19.2,
      "Smoking": "No",
      "AlcoholDrinking": "No",
      "Stroke": "No",
      "PhysicalHealth": 7,
      "MentalHealth": 2,
      "DiffWalking": "No",
      "Sex": "Male",
      "AgeCategory": "18-24",
      "Race": "Asian",
      "Diabetic": "No",
      "PhysicalActivity": "Yes",
      "GenHealth": "Good",
      "SleepTime": 6,
      "Asthma": "Yes",
      "KidneyDisease": "No",
      "SkinCancer": "No"
    }
    console.log(data)
    let res = await axios.post("http://localhost:5000/predict", data)
    console.log(res)
  }

  return (
    <>
      <form onSubmit={handleSumbit}>
        <button type="submit">Send</button>
      </form>
    </>
  )
}

export default App
