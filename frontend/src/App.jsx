import axios from "axios"

function App() {
  const handleSumbit = async (e) => {
    e.preventDefault()
    let data = {
      "BMI": 29.2,
      "Smoking": "Yes",
      "AlcoholDrinking": "Yes",
      "Stroke": "No",
      "PhysicalHealth": 20,
      "MentalHealth": 12,
      "DiffWalking": "No",
      "Sex": "Male",
      "AgeCategory": "75-79",
      "Race": "White",
      "Diabetic": "No",
      "PhysicalActivity": "Yes",
      "GenHealth": "Good",
      "SleepTime": 6,
      "Asthma": "No",
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
