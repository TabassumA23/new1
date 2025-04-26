export interface User {
    id: number;
    api: string;
    first_name: string;
    last_name: string;
    email: string;
    date_of_birth: number;
    password: string;
    userType: string;
    restaurant: Restaurant[];
}

export interface Restaurant {
    id: number;
    api: string;
    name: string;
    description: string;
}
export interface Recommendation{
    id:number;
    api: string;
    name: string;
    restaurant: string;
}

export interface Review {
    id: number;
    api: string;
    user: number;
    name: string;
    description: string;
}

export interface Wishlist {
    id: number;
    api: string;
    user: number;
    name: string;
    description: string;
}
export interface WishlistItem {
    id: number;
    api: string;
    user: number;
    name: string;
    description: string;
}

export interface Cuisine {
    id: number;
    api: string;
    name: string;
}
export interface Allergy {
    id: number;
    api: string;
    name: string;
}

export interface Friendship{
    id: number;
    api: string;
    user: number;
    friend: number;
    username: string;
    accepted: boolean;
}

export interface Chosen{
    id: number;
    api: string;
    user: number;
    restaurant: number;
    name: string;
}

export interface ChosenCuisine{
    id: number;
    api: string;
    user: number;
    cusine: number;
    name: string;
}
export interface ChosenAllergy{
    id: number;
    api: string;
    user: number;
    allergy: number;
    name: string;
}
export interface Reservation {
    id: number;
    api: string;
    restaurant: Restaurant;  
    user: User;
    reservation_time: string;  
    number_of_people: number;
    status: string; 
    special_requests: string;
}

