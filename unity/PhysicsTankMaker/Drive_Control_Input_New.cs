using UnityEngine;
using UnityEngine.InputSystem;
using Unity.Linq;
using System.Linq;
using ScriptableObjectArchitecture;

namespace ChobiAssets.PTM
{
	public class Drive_Control_Input_New : Drive_Control_Input_03_Single_Stick_CS
	{
		private InputAction driveAction;
		private Camera camera;
		private Transform mainBody;
		
		private TankInputConfig tankInputConfig;
		
		// Awake is called when the script instance is being loaded.
		protected void Awake()
		{
			driveAction = InputSystem.actions["Move"];
			
			tankInputConfig = Resources.Load<TankInputConfig>("TankInput");
		}
		
		// Start is called on the frame when a script is enabled just before any of the Update methods is called the first time.
		protected void Start()
		{
			var root = gameObject.Ancestors().Last();
			camera = root.GetComponentInChildren<Camera_Points_Manager_CS>().GetComponentInChildren<Camera>();
		}
		
		// Implement OnDrawGizmos if you want to draw gizmos that are also pickable and always drawn.
		protected void OnDrawGizmos()
		{
			if (camera != null)
			{
				Gizmos.color = Color.green;
				Gizmos.DrawSphere(camera.transform.position, 0.5f);
			}
		}
		
		// OnGUI is called for rendering and handling GUI events.
		protected void OnGUI()
		{
			GUIStyle style = new GUIStyle();
			style.normal.textColor = Color.blue;
			GUILayout.BeginArea(new Rect(100, 100, 100, 40));
			GUILayout.Label($"axis {axis.x:F2} {axis.y:F2}", style);
			GUILayout.EndArea();
		}
		
		private Vector2 axis;
		private float gear = 0.5f;
		private float turnBrakeRate = 0.4f;
		
		public override void Drive_Input()
		{
			axis = driveAction.ReadValue<Vector2>();
			//if (Mathf.Abs(axis.x) < 0.05f)
			//{
			//	axis.x = 0;
			//}
			
			//if (Mathf.Abs(axis.y) < 0.05f)
			//{
			//	axis.y = 0;
			//}
			
			//axis.Normalize();

			// Set the "Stop_Flag", "L_Input_Rate", "R_Input_Rate" and "Turn_Brake_Rate".
			Set_Values();
		}
		
		protected override void Set_Values()
		{
			if (axis.magnitude == 0) {
				controlScript.Stop_Flag = true;
				controlScript.L_Input_Rate = 0;
				controlScript.R_Input_Rate = 0;
				return;
			}
			
			controlScript.Stop_Flag = false;
			
			Vector2 localAxis = Utils.ConvertVirtualDir(camera.transform, transform, axis);
			
			if (axis.y == 0) {
				float angle = Vector2.SignedAngle(localAxis, Vector2.up);
				if (Mathf.Abs(angle) <= 90) {
					controlScript.L_Input_Rate = -gear;
					controlScript.R_Input_Rate = gear;
					if (Mathf.Abs(angle) < 2) {
						controlScript.Turn_Brake_Rate = 0;
					}
					else {
						float t = Mathf.Abs(angle) / 90;
						float t1 = tankInputConfig.turnBrakeCurve.Evaluate(1-t);
						controlScript.Turn_Brake_Rate = Mathf.Sign(angle) * turnBrakeRate * t1;
						ConsoleProDebug.Watch("info", $"t = {t:F2}, t1 = {t1:F2}, rate = {controlScript.Turn_Brake_Rate}");
					}
				}
				else {
					controlScript.L_Input_Rate = gear;
					controlScript.R_Input_Rate = -gear;
					if (Mathf.Abs(angle) > 178) {
						controlScript.Turn_Brake_Rate = 0;
					}
					else {
						float t = (180 - Mathf.Abs(angle)) / 90;
						float t1 = tankInputConfig.turnBrakeCurve.Evaluate(1-t);
						controlScript.Turn_Brake_Rate = Mathf.Sign(angle) * turnBrakeRate * t;
						ConsoleProDebug.Watch("info", $"t = {t:F2}, t1 = {t1:F2}, rate = {controlScript.Turn_Brake_Rate}");
					}
				}
			}
			else if (axis.y > 0) {
				float angle = Vector2.SignedAngle(localAxis, Vector2.up);
				if (Mathf.Abs(angle) <= 135) {
					controlScript.L_Input_Rate = -gear;
					controlScript.R_Input_Rate = gear;
					if (Mathf.Abs(angle) < 2) {
						controlScript.Turn_Brake_Rate = 0;
					}
					else {
						float t = Mathf.Abs(angle) / 135;
						t = tankInputConfig.turnBrakeCurve.Evaluate(1-t);
						controlScript.Turn_Brake_Rate = Mathf.Sign(angle) * turnBrakeRate * t;
					}
				}
				else {
					controlScript.L_Input_Rate = gear;
					controlScript.R_Input_Rate = -gear;
					if (Mathf.Abs(angle) > 178) {
						controlScript.Turn_Brake_Rate = 0;
					}
					else {
						float t = (180 - Mathf.Abs(angle)) / 45;
						t = tankInputConfig.turnBrakeCurve.Evaluate(1-t);
						controlScript.Turn_Brake_Rate = Mathf.Sign(angle) * turnBrakeRate * t;
					}
				}
			}
			else {
				float angle = Vector2.SignedAngle(localAxis, Vector2.up);
				if (Mathf.Abs(angle) <= 45) {
					controlScript.L_Input_Rate = -gear;
					controlScript.R_Input_Rate = gear;
					if (Mathf.Abs(angle) < 2) {
						controlScript.Turn_Brake_Rate = 0;
					}
					else {
						float t = Mathf.Abs(angle) / 45;
						t = tankInputConfig.turnBrakeCurve.Evaluate(1-t);
						controlScript.Turn_Brake_Rate = Mathf.Sign(angle) * turnBrakeRate * t;
					}
				}
				else {
					controlScript.L_Input_Rate = gear;
					controlScript.R_Input_Rate = -gear;
					if (Mathf.Abs(angle) > 178) {
						controlScript.Turn_Brake_Rate = 0;
					}
					else {
						float t = (180 - Mathf.Abs(angle)) / 135;
						t = tankInputConfig.turnBrakeCurve.Evaluate(1-t);
						controlScript.Turn_Brake_Rate = Mathf.Sign(angle) * turnBrakeRate * t;
					}
				}
			}
			
			//controlScript.L_Input_Rate = tankInputConfig.lInputRate;
			//controlScript.R_Input_Rate = tankInputConfig.rInputRate;
			//if (tankInputConfig.dInputRate != 0) {
			//	controlScript.L_Input_Rate = -tankInputConfig.dInputRate;
			//	controlScript.R_Input_Rate = tankInputConfig.dInputRate;
			//}
			//controlScript.Turn_Brake_Rate = tankInputConfig.turnBrakeRate;
			//controlScript.Pivot_Turn_Flag = tankInputConfig.pivotTurnFlag;
			//controlScript.Stop_Flag = tankInputConfig.stopFlag;
		}
	}
}

