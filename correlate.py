import math
import sys
import time

def LoadData(filename):
  # This function reads the data from the MovieLens dataset and returns a
  # dictionary populated with all of the data.  The dictionary keys are the
  # integer user ids, and the values are a list containing the average ranking
  # and a dictionary with the rankings.  The rankings dictionary has keys
  # which are the integer movie ids and the values are the integer movie
  # rankings.

  # Start with an empty dictionary for the users and their data
  users = {} 

  f = open(filename)

  nlines = 0
  for line in f:
    # Split the line into user, movie, and ranking
    fields  = line.split()
    userid  = int(fields[0])
    movieid = int(fields[1])
    ranking = int(fields[2])

    if userid in users:
      # Existing user, add to their existing data
      users[userid][1][movieid] = ranking
    else:
      # New user, add them to the dictionary
      users[userid] = [-1., {movieid: ranking}]

    nlines += 1

  f.close()

  # Compute the average movie ranking for each user
  for userid in users:
    rankings = users[userid][1]
    total = 0.
    for movieid in rankings:
      total += rankings[movieid]
    users[userid][0] = total/len(rankings)
 
  print "Read %d lines from file %s" % (nlines, filename)
  print "Total of %d users" % len(users)

  return users


def ComputePCC(user1, user2):
  # Computes the Pearson Correlation Coefficient for two users based on the
  # movies for which they have both provided a ranking.  Returns the PCC and
  # the number of commonly ranked movies.

  avg1      = user1[0]
  rankings1 = user1[1]
  avg2      = user2[0]
  rankings2 = user2[1]

  # Find movies ranked by both users
  movies = set(rankings1.keys()) & set(rankings2.keys())
  ncommon = len(movies)

  # Compute numerator and denominator terms
  num     = 0.  # numerator
  den1    = 0.  # denominator term for user1
  den2    = 0.  # denominator term for user2

  for movieid in movies:
    num += (rankings1[movieid] - avg1)*(rankings2[movieid] - avg2)
    den1 += math.pow(rankings1[movieid] - avg1, 2)
    den2 += math.pow(rankings2[movieid] - avg2, 2)

  # Compute Pearson Correlation Coefficient.  The 1.e-6 in the denominator is
  # to avoid division by zero.
  pcc = num/math.sqrt(den1*den2+1.e-6)

  return pcc, ncommon


def ComputeCorrelations(users, filename, threshold):
  # Computes the correlations between a set of users using the Pearson
  # Correlation Coefficient and for each user outputs the best positive
  # correlation, assuming they have rated at least threshold movies in common.

  t0 = time.time()
  f = open(filename, "w")

  # Loop over users and compute the best positive correlation for user1.  Sort
  # the keys to ensure the output file is in order.
  for id1 in sorted(users):
    user1 = users[id1]

    # Initialize a tuple to hold the current best correlated user. After comparing
    # user1 to all other users, this will hold the best positive correlation.
    # Note that this tuple may still be empty at the end, if user1 didn't have
    # threshold movies in common with any other users.
    bestcorrelation = ()

    # Compare user1 against all other users
    for id2 in users:
      # Skip case where user1 and user2 are the same
      if id1 == id2:
        continue

      # Compute the correlation and number of commonly rated movies
      user2 = users[id2]
      pcc, ncommon = ComputePCC(user1, user2)

      # Make sure the threshold for minimum number of common movies was met
      if ncommon >= threshold:
        # Save this correlation if it is better than the existing one, or if
        # the best correlation is currently empty
        if (bestcorrelation and pcc > bestcorrelation[1]) or (not bestcorrelation):
          bestcorrelation = (id2,pcc,ncommon)

    # Write the result for user1 to the output file
    if bestcorrelation:
      # Best positive correlation
      f.write("%d (%d,%.2f,%d)\n" % ((id1,) + bestcorrelation))
    else:
      # No correlation
      f.write("%d\n" % id1)

  f.close()
  t1 = time.time()
  print("Computed correlations in %f seconds" % (t1-t0))
  return

# Begin execution
if __name__ == "__main__":
  if len(sys.argv) < 3:
    print "Usage:"
    print "  python %s <movie data> <correlations file> [threshold]" % sys.argv[0]
    sys.exit()

  moviedatafile = sys.argv[1]
  correlationsfile = sys.argv[2]

  # Threshold for minimum number of common movies
  if len(sys.argv) == 4:
    threshold = int(sys.argv[3])
  else:
    threshold = 6

  # Load the data and compute correlations
  users = LoadData(moviedatafile)
  ComputeCorrelations(users, correlationsfile, threshold)
