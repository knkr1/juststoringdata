import java.util.Scanner;

public class Main {
    public static void main(String[] args){
        Scanner input = new Scanner(System.in);
        int sum = 0;
        int[] RandomDimension= {0,0,0,0,0,0};
        while(true){
            System.out.print("Zar atmak için Enter'a bas!");
            input.nextLine();
            int RandomInt = (int)(Math.random()*6)+1;

            sum += RandomInt;
            RandomDimension[RandomInt-1]+=1;

            for(int i = 0;i<=5;i++){
                System.out.print(" ");
            }
            System.out.print(RandomInt);
            for(int i = 0;i<=5;i++){
                System.out.print(" ");
            }
            System.out.println();
            for(int i = 0;i<=5;i++){
                System.out.print(RandomDimension[i]);
                System.out.print(" ");
            }
            System.out.print(sum);
            System.out.println();
            
        }
    }
}
