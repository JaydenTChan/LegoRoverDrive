package newproject;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

import lejos.hardware.Button;
import lejos.hardware.motor.UnregulatedMotor;
import lejos.hardware.port.MotorPort;

public class multiPC {

	// === Network Variables
	// Change this to match port on PC
	public static int port = 5001;
	
	public static BufferedReader in;
	public static DataOutputStream out;
	public static ServerSocket serv;
	public static Socket s;
	
	public static String action;
	public static String action2;
	
	public static UnregulatedMotor[] UM = new UnregulatedMotor[4];
	
	public static int[] MP = {0,0,0,0};
	public static int[] ang = {0,0,0,0};
	public static boolean[] angLock = {false, false, false, false};
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		
		try {
			serv = new ServerSocket(port);
			System.out.println("Waiting for connection...");
			s = serv.accept(); //Wait for Lap top to connect
			System.out.println("Connected!");
			in = new BufferedReader(new InputStreamReader(s.getInputStream()));
			out = new DataOutputStream(s.getOutputStream());
		}catch(IOException ioe){
			System.out.println("Error in connection");
		}
		
		boolean exit = false;
		
		while(Button.getButtons() == 0 && exit == false){
			
			try {
				if(in.ready()) {
					action = in.readLine();
					System.out.println(action);
					
					switch(action){
						case "1":
							//Change Motor Speed
							action = in.readLine();
							motor(action);
							break;
						case "2":
							//Disconnect
							exit = true;
							break;
						case "3":
							//Change Angle
							action = in.readLine();
							changeAngle(action);
							break;
						default:
							System.out.println("You shouldn't be here");
							break;
					}//End switch
				}//End if
				
				// === For loop for setting speed and dealing with angle constraints === //
				for (int i = 0; i < MP.length ; i++) {
					
					if(UM[i] != null) {UM[i].setPower(MP[i]);}
					
					if(angLock[i] == true) {
						
						if (MP[i] > 0) {
							if(UM[i].getTachoCount() >= ang[i]) {
								MP[i] = 0;
							}
						}else if (MP[i] < 0){
							if(UM[i].getTachoCount() <= ang[i]) {
								MP[i] = 0;
							}
						}else {
							MP[i] = 0;
						}
						
					}
				}//End For
				
			}catch(IOException ioe) {
				System.out.println(ioe);
			}
			
		}//Wait for button to end program.
		try {
			serv.close();
		}catch(IOException ioe) {
			System.out.println("Could not close socket!");
		}
	}
	
	public static int toNumber(String let) {
		int res;
		switch(let) {
			case "A":
				res = 0;
				break;
			case "B":
				res = 1;
				break;
			case "C":
				res = 2;
				break;
			case "D":
				res = 3;
				break;
			default:
				res = 0;
				break;
		}
		return res;
	}
	
	public static void initMotor(int index) {
		switch(index) {
			case 0:
				UM[index]=new UnregulatedMotor(MotorPort.A);
				break;
			case 1:
				UM[index]=new UnregulatedMotor(MotorPort.B);
				break;
			case 2:
				UM[index]=new UnregulatedMotor(MotorPort.C);
				break;
			case 3:
				UM[index]=new UnregulatedMotor(MotorPort.D);
				break;
			default:
				System.out.println("Error initializing motor");
				break;
		}
		UM[index].resetTachoCount();
	}
	
	public static void motor(String mot) {
		int index = toNumber(mot);
		try {
			if(UM[index] == null) {initMotor(index);}
			action = in.readLine();
			MP[index] = Integer.parseInt(action);
			angLock[index] = false;
		}catch(IOException ioe) {
			System.out.println(ioe);
		}
	}
	
	public static void changeAngle(String mot) {
		
		motor(mot);
		int index = toNumber(mot);
		
		try {
			UM[index].resetTachoCount();
			action = in.readLine();
			angLock[index] = true;
			ang[index] = Integer.parseInt(action);
		}catch(IOException ioe) {
			System.out.println(ioe);
		}
		System.out.println("Done Angle");
	}

}

