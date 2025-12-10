

export interface GamificationEntity {
    id?: number;
    User_email: string;
    level: number;
    total_experience_points: number;

}

export interface MenuItem {
    id?: number;
    name: string;
    price: number;
    description?: string;
    quantity?: number;
}

export interface OrderRequestBody {
     selectedItems: MenuItem[],
     name: string,
     surname: string,
     email: string,
     address: 'Some address'
}