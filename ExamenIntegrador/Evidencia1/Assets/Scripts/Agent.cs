using UnityEngine;
using System.Collections.Generic;

public class Agent : MonoBehaviour
{
    private Queue<Vector3> waypointQueue = new Queue<Vector3>();
    public float moveSpeed = 10.0f; // Speed of movement

    // Start is called once before the first execution of Update after the MonoBehaviour is created
 
    // Update is called once per frame
    void Update()
    {
        // Move the object towards the next waypoint
        if (waypointQueue.Count > 0)
        {
            Vector3 target = waypointQueue.Peek();
            float step = moveSpeed * Time.deltaTime;

            // Move towards the waypoint
            transform.position = Vector3.MoveTowards(transform.position, target, step);

            // If the object reaches the waypoint, remove it from the queue
            if (Vector3.Distance(transform.position, target) < 0.1f)
            {
                waypointQueue.Dequeue();
            }
        }
    }

    public void SetWaypoint(Vector3 waypoint)
    {
        waypointQueue.Enqueue(waypoint);
        Debug.Log("Waypoint added. Queue size: " + waypointQueue.Count);
    }
}
