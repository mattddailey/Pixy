import axios from 'axios'

const api = axios.create({
    baseURL: process.env.REACT_APP_BASE_URL + ":5000",
})

const FlaskService = {

    getBrightness: async function() {
        try {
            const response = await api.get("/brightness");
            return response.data.brightness
        } catch(error) {
            console.log(error)
        }
    },

    getMode: async function() {
        try {
            const response = await api.get("/mode");
            return response.data
        } catch(error) {
            throw error
        }
    },

    getPrimaryColor: async function() {
        try {
            const response = await api.get("/primary_color");
            return response.data
        } catch(error) {
            throw error
        }
    },

    setBrightness: async function(brightness) {
        try {
            const json = { 
                "utility" : "brightness",
                "brightness" : brightness
                }
            await api.post("/utility", json)
        } catch(error) {
            console.log(error)
        }
    },

    setPrimaryColor: async function(red, green, blue) {
        try {
            const json = { 
                "utility" : "primary_color",
                "red" : red,
                "green" : green,
                "blue" : blue
                }
            console.log(json)
            await api.post("/utility", json)
        } catch(error) {
            console.log(error)
        }
    },

    setMode: async function(mode) {
        try {
            await api.post("/mode/" + mode);
        } catch(error) {
            throw error
        }
    }
}

export default FlaskService;
