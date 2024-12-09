<template>
	<v-container>
		<v-row v-if="users && users.length > 0">
			<v-col
				v-for="user in users"
				:key="user.id"
				cols="12"
			>
				<v-card>
					<v-card-title>{{ user.name }}</v-card-title>
					<v-card-subtitle>{{ user.email }}</v-card-subtitle>
					<v-card-text>
						Username: {{ user.username }} <br />
						Website: {{ user.website }}
					</v-card-text>
				</v-card>
			</v-col>
		</v-row>
		<p v-else>No users found</p>
	</v-container>
	<v-container class="d-flex align-center justify-center" style="height: 100vh">
		<v-progress-circular indeterminate color="primary" />
		<p class="ml-3">Loading users...</p>
	</v-container>
</template>

<script>
import { useUserStore } from "@/stores/users";

export default {
  name: "TestApi",
  async setup() {
    // Access the user store
    const userStore = useUserStore();

    // Fetch users when the component is mounted
    console.log("Calling fetchUsers");
    await userStore.fetchUsers(); // Fetch and wait

    // console.log("Yo!");
    // console.log("Hello there!", userStore.getUsers);

    // Expose state and getters to the template
    return {
      users: userStore.getUsers,
    };
  },
};
</script>
