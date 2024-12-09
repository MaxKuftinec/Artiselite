<template>
  <v-layout>
		<v-navigation-drawer style="border: 1px solid blue; z-index: 99;">
      <v-list density="compact" item-props :items="items" nav />

      <template #append>
        <v-list-item
          class="ma-2"
          link
          nav
          prepend-icon="mdi-cog-outline"
          title="Settings"
        />
      </template>
    </v-navigation-drawer>
		</v-layout>
		<v-container>
    <v-card class="pa-4 justify-center">
      <v-card-title>User Management</v-card-title>
      <v-card-text>
        <!-- Only allow user creation if the current user is an admin -->
        <div v-if="currentUser.role_id === 0">
          <h3>Create User</h3>
          <v-form @submit.prevent="createUser" v-model="formValid">
            <v-text-field
              label="Username"
              v-model="newUser.username"
              :rules="[rules.required]"
              outlined
            ></v-text-field>
            <v-text-field
              label="Password"
              v-model="newUser.password"
              :rules="[rules.required]"
              type="password"
              outlined
            ></v-text-field>
            <v-select
              label="Role"
              v-model="newUser.role_id"
              :items="roles"
              item-title="text"
              item-value="value"
              outlined
            ></v-select>
            <v-btn
              :disabled="!formValid"
              class="mt-4"
              color="primary"
              type="submit"
            >
              Create User
            </v-btn>
						<v-btn class="mt-4 ml-4" color="primary" to="/">Home</v-btn>
          </v-form>
          <p v-if="errorMessage" class="error-text">{{ errorMessage }}</p>
        </div>

        <!-- Display current user details -->
        <h3>Current User</h3>
        <p>Username: {{ currentUser.username }}</p>
        <p>Role: {{ roleName(currentUser.role_id) }}</p>
      </v-card-text>
    </v-card>
	</v-container>
  
</template>

<script>
import { useUserStore } from "@/stores/users";
import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL;

export default {
  data() {
    return {
      currentUser: {},
      newUser: {
        username: "",
        password: "",
        role_id: null,
      },
      roles: [
        { text: "Admin", value: 0 },
        { text: "Manager", value: 1 },
        { text: "Operator", value: 2 },
      ],
      errorMessage: "",
      formValid: false,
      rules: {
        required: (value) => !!value || "This field is required.",
      },
			items: [
					{
						title: 'Inventory',
						prependIcon: 'mdi-view-dashboard-outline',
						to: '/inventory'
					},
					{
						title: 'Team',
						prependIcon: 'mdi-account-group',
						to: '/team'
					},
					{
						title: 'Inbound',
						prependIcon: 'mdi-bank-transfer-in',
						to: '/projects'
					},
					{
						title: 'Outbound',
						prependIcon: 'mdi-bank-transfer-out',
						to: '/calendar'
					},
					{
						title: 'Reports',
						prependIcon: 'mdi-file-chart-outline',
						to: '/reports'
					}
				],
    };
  },
  methods: {
    async fetchCurrentUser() {
			const userStore = useUserStore();


			await userStore.fetchUserInfo(); // Initialized the user
			this.currentUser = userStore.user;
			console.log(this.currentUser);
    },
    async createUser() {
      try {
        await axios.post(
          `${API_BASE_URL}/users`,
          { ...this.newUser },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem("token")}`,
            },
          }
        );
        alert("User created successfully!");
        this.newUser = { username: "", password: "", role_id: null };
      } catch (error) {
        this.errorMessage = "Failed to create user.";
      }
    },
    roleName(roleId) {
      const role = this.roles.find((r) => r.value === roleId);
      return role ? role.text : "Unknown";
    },
  },
  mounted() {
    this.fetchCurrentUser();
  },
};
</script>

<style scoped>
.error-text {
  color: red;
  font-size: 0.9rem;
}
</style>
