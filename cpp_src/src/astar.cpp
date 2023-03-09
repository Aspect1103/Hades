// Std includes
#include <queue>
#include <stdexcept>
#include <unordered_map>

// Custom includes
#include "astar.hpp"
#include "primitives.hpp"

// ----- STRUCTURES ------------------------------
/// Represents a grid position and its costs from the start position
///
/// Parameters
/// ----------
/// cost - The cost to traverse to this neighbour.
/// destination - The destination point in the grid.
struct Neighbour {
  int cost;
  Point destination;

  inline bool operator<(const Neighbour nghbr) const {
    // The priority_queue data structure gets the maximum priority, so we need
    // to override that functionality to get the minimum priority
    return cost > nghbr.cost;
  }
};

// ----- CONSTANTS ------------------------------
// Represents the north, south, east, west, north-east, north-west, south-east and south-west directions on a compass
const std::vector<Point> INTERCARDINAL_OFFSETS = {
    {-1, -1}, {0, -1}, {1, -1}, {-1, 0}, {1, 0}, {-1, 1}, {0, 1}, {1, 1},
};

// ----- FUNCTIONS ------------------------------
std::vector<Point>
calculate_astar_path(std::vector<std::vector<TileType>> &grid, const Point start, const Point end) {
  // Check if the grid size is not zero, if not, set up a few variables needed
  // for the pathfinding
  if (grid.empty()) {
    throw std::length_error("Grid size must be bigger than 0.");
  }
  std::vector<Point> result;
  std::priority_queue<Neighbour> queue;
  std::unordered_map<Point, Neighbour> neighbours = {{start, {0, start}}};
  Point grid_size = {(int) grid[0].size(), (int) grid.size()};
  queue.push({0, start});

  // Loop until the priority queue is empty
  while (!queue.empty()) {
    // Get the lowest cost pair from the priority queue
    Point current = queue.top().destination;
    queue.pop();

    // Check if we've reached our target
    if (current == end) {
      // Backtrack through came_from to get the path
      while (!(neighbours[current].destination == current)) {
        // Add the current pair to the result list
        result.emplace_back(current.x, current.y);

        // Get the next pair in the path
        current = neighbours[current].destination;
      }

      // Add the start pair and exit out of the loop
      result.emplace_back(start.x, start.y);
      break;
    }

    // Add all the neighbours to the heap with their cost being f = g + h:
    //   f - The total cost of traversing the neighbour.
    //   g - The distance between the start pair and the neighbour pair.
    //   h - The estimated distance from the neighbour pair to the end pair.
    //   We're using the Chebyshev distance for this.
    for (Point offset : INTERCARDINAL_OFFSETS) {
      // Calculate the neighbour's position and check if its valid excluding the
      // boundaries as that produces weird paths
      Point neighbour = current + offset;
      if (neighbour.x < 0 || neighbour.x >= grid_size.x || neighbour.y < 0 || neighbour.y >= grid_size.y) {
        continue;
      }

      // Test if the neighbour is an obstacle or not. If so, skip to the next
      // neighbour as we want to move around it
      if (grid[neighbour.y][neighbour.x] == TileType::Obstacle) {
        continue;
      }

      // Calculate the distance from the start
      int distance = neighbours[current].cost + 1;

      // Check if we need to add a new neighbour to the heap
      if ((!neighbours.contains(neighbour)) || distance < neighbours[neighbour].cost) {
        neighbours[neighbour] = {distance, current};

        // Add the neighbour to the priority queue
        // TODO: DECIDE BETWEEN MANHATTAN AND CHEBYSHEV (PROBABLY CHEBYSHEV DUE TO WACKY HALLWAYS)
        // (abs(end.x - neighbour.x) + abs(end.y - neighbour.y))
        queue.push({distance + std::max(abs(end.x - neighbour.x), abs(end.y - neighbour.y)), neighbour});
      }
    }
  }

  // Return result
  return result;
}