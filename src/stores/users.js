import { defineStore } from "pinia";
import axios from "axios";

// export const useUserStore = defineStore('user', {
// 	state: () => ({
// 		users: []
// 	}),

// 	getters: {
// 		getUsers: (state) => state.users
// 	},

// 	actions: {
// 		async fetchUsers() {
// 			console.log("Insides fetchUsers of users.js");
// 			try {
// 				const response = await axios.get("https://jsonplaceholder.typicode.com/users");
// 				this.users = response.data;
// 				console.log("Data fetched successfully. The users are:");
// 				console.log(this.users)
// 			}
// 			catch (error) {
// 				console.error("Error fetching users in store:", error);
// 			}
// 		}
// 	}
// })

const API_BASE_URL = import.meta.env.VITE_API_URL;
console.log("Inside users.js");
export const useUserStore = defineStore('user', {
	state: () => ({
		user: null, // Store authenticated user detail
		token: null,
		isAuthenticated: false,
	}),

	getters: {
		getUser: (state) => state.user,
		isLoggedIn: (state) => state.isAuthenticated
	},

	actions: {
		async	login(username, password) {
			try {
				const response = await axios.post(`${API_BASE_URL}/token`, {username, password}, {headers: {"Content-Type": "application/x-www-form-urlencoded"}}); // I don't truly understand the header part

				this.token = response.data.access_token;
				this.isAuthenticated = true;
				axios.defaults.headers.common['Authorization'] = `Bearer ${this.token}`; // What exactly is this?

				localStorage.setItem('token', this.token);

				await this.fetchUserInfo(); // Fetch user details after login				
			}
			catch (error) {
				console.error("Error during login:", error);
				throw new Error("Invalid username or password");
			}
		},

		async fetchUserInfo() {
			try {
				const	response = await axios.get(`${API_BASE_URL}/me`, {headers: {Authorization: `Bearer ${this.token}`}});

				this.user = response.data;
			}
			catch (error) {
				console.error("Error fetching user info", error);
				this.logout();
			}
		},

		logout() {
			this.user = null;
			this.token = null;
			this.isAuthenticated = false;
			localStorage.removeItem('token');
			axios.defaults.headers.common['Authorization'] = null; // Clearing token?
		}
	}
})