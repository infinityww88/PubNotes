using UnityEngine;

public static class Utils
{
	public static Vector2 ConvertVirtualDir(Transform A, Transform B, Vector2 dir)
	{
		Vector3 forward = A.forward;
		forward.y = 0;
		forward.Normalize();
		Quaternion rot = Quaternion.FromToRotation(Vector3.forward, forward);
		Vector3 dir3d = new Vector3(dir.x, 0, dir.y);
		dir3d = rot * dir3d;
			
		forward = B.forward;
		forward.y = 0;
		forward.Normalize();
		rot = Quaternion.FromToRotation(forward, Vector3.forward);
		dir3d = rot * dir3d;
		dir.x = dir3d.x;
		dir.y = dir3d.z; 
		return dir;
	}
}
