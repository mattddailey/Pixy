import axios from 'axios'

const api = axios.create({
    baseURL: "http://10.0.0.198:5000",
})

const FlaskService = {

    startSpotify: async function() {
        try {
            await api.get("/spotify");
            return
        } catch(error) {
            throw error
        }
    },

    revoke: async function() {
        try {
            await api.get("/revoke");
            return
        } catch(error) {
            throw error
        }
    },
    
    getCurrentMode: async function() {
        try {
            const response = await api.get("/currentMode");
            return response.data
        } catch(error) {
            throw error
        }
    },
    
    getIsSpotifyAuthorized: async function() {
        try {
            const response = await api.get("/isLoggedIn");
            return response.data
        } catch(error) {
            throw error
        }
    }
}

export default FlaskService;