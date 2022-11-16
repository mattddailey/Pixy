import axios from 'axios'

const api = axios.create({
    baseURL: process.env.REACT_APP_BASE_URL + ":5000",
})

const FlaskService = {

    setMode: async function(mode) {
        try {
            await api.post("/mode/" + mode);
            return
        } catch(error) {
            throw error
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
