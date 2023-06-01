from functools import wraps

# requires resource manager permission
# 
# also ... security permissions, access controller permission to execute script

class executor:
    def __init__(self, constraint):
        self.constraint = constraint

    def __call__(self, func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            # Assuming the first argument is the instance of the class (self)
            instance = args[0]

            # Check if mas_energy_budget is greater than the threshold
            mas_energy_budget = instance.db['mas_energy_budget'].find_one()
            mas_energy_budget_min_threshold = instance.db['mas_energy_budget_min_threshold'].find_one()
            
            if mas_energy_budget > mas_energy_budget_min_threshold:
                # Broadcast pre-run result
                instance.messenger.broadcast({'status': 'pre-run', 'mas_energy_budget': mas_energy_budget})

                # Execute function and get result
                result = func(*args, **kwargs)

                # Recalculate mas_energy_budget
                mas_energy_budget = instance.db['mas_energy_budget'].find_one()
                if mas_energy_budget < mas_energy_budget_min_threshold:
                    raise Exception("MAS energy budget below minimum threshold!")

                # Broadcast post-run result
                instance.messenger.broadcast({'status': 'post-run', 'result': result})
                return result
            else:
                raise Exception("MAS energy budget below minimum threshold!")

        return wrapped_func
