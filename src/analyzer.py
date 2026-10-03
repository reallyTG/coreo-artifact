from analyzer_library import InfoStorage, FunctionRunSummary, FunctionInputInfo, Metric, Feature

import sys
import random
import os

# imports for plots
import matplotlib.pyplot as plt
import numpy as np
import big_o
import statsmodels.api as sm

from core import model_fit
import scipy.stats as ss
import math
import re

from core.plots import autoscale_y

class Analyzer:
    def __init__(self, names = [], summaries = {}) -> None:
        self.names = names
        self.summaries = summaries
        self.metrics = []
        self.features = []
        self.requests = []
        self.function_names = {}
        self.storage = None
        # name -> legend/filename label. A name is a storage key (a CSV path,
        # or a CSV path plus a categorical value) and is not printable.
        self.name_labels = {}

    def read_csvs(self, 
                  file_names = [], 
                  metrics = ["runtime_ns", "memory_peak"], 
                  categoricals = [], 
                  input_features = ["length"], 
                  ignore = ["memory_after"], 
                  prop_filters = [],
                  metric_filters = [],
                  grab_every = 1, 
                  input_dir = None):
        # filters is a list of tuples, where each tuple is (feature_name, value); do not add an entry if the feature_name has the value
        if len(categoricals) == 0:
            self.names = file_names
        else:
            self.names = []
        self.summaries = dict()
        self.metrics = metrics

        for file_name in file_names:
            # to deal with categoricals, we might update the summary_file_names with each category
            # e.g., if we have a category "C" with values "a" and "b" with file name "n", we might have summary_file_names = ["n-C/a", "n-C/b"]
            summary_file_names = []

            try:
                with open(file_name, 'r') as file:
                    summaries = []
                    input_feature_names = []
                    first_line = True
                    data_mapping = {
                        "function_name": -1,
                        "input_id": -1,
                    }
                    index = 0
                    for line in file:
                        # trim newline
                        line = line.strip()
                        # handle header
                        if first_line:
                            # split by commas
                            header_contents = line.split(',')
                            if "function_name" in header_contents:
                                data_mapping["function_name"] = header_contents.index("function_name")
                            if "input_id" in header_contents:
                                data_mapping["input_id"] = header_contents.index("input_id")

                            for metric in metrics:
                                if metric in header_contents:
                                    data_mapping[metric] = header_contents.index(metric)
                                else:
                                    print(f"Metric '{metric}' not found in '{file_name}'.")
                                    print(f"Specify metrics when you begin analysis.")
                                    sys.exit(1)
                            
                            for categorical in categoricals:
                                if categorical in header_contents:
                                    data_mapping[categorical] = header_contents.index(categorical)
                                else:
                                    print(f"Categorical '{categorical}' not found in '{file_name}'.")
                                    print(f"Specify categoricals when you begin analysis.")
                                    sys.exit(1)

                            # for all unaccounted for columns, assume they are input features
                            for i in range(len(header_contents)):
                                if header_contents[i] in ignore:
                                    continue
                                if i not in data_mapping.values():
                                    input_feature_names.append(header_contents[i])
                                    data_mapping[header_contents[i]] = i

                            first_line = False
                            continue

                        index += 1
                        if index % grab_every != 0:
                            continue

                        # split by commas
                        data = line.split(',')
                        # create a new summary
                        # first, collect function info, if any
                        function_name = "function"
                        input_id = "-1"
                        if data_mapping["function_name"] != -1:
                            function_name = data[data_mapping["function_name"]]
                        if data_mapping["input_id"] != -1:
                            input_id = data[data_mapping["input_id"]]
                        fn_input_info = FunctionInputInfo(function_name, input_id)

                        # then, collect metrics
                        metrics_list = []
                        skip_line = False
                        for metric in metrics:
                            for (mn, fn) in metric_filters:
                                if mn == metric and fn(float(data[data_mapping[metric]])):
                                    print(f"Skipping line with {metric} = {data[data_mapping[metric]]}.")
                                    skip_line = True
                            metrics_list.append(Metric(metric, data[data_mapping[metric]]))
                        # then, collect input features
                        features_list = []
                        for feature_name in input_feature_names:
                            for (ff, fn) in prop_filters:
                                if ff == feature_name and fn(float(data[data_mapping[feature_name]])):
                                    print(f"Skipping line with {feature_name} = {data[data_mapping[feature_name]]}.")
                                    skip_line = True
                            features_list.append(Feature(feature_name, data[data_mapping[feature_name]]))
                        if skip_line:
                            continue
                        # then, collect categoricals
                        # if there are categoricals...
                        row_names = []
                        if len(categoricals) > 0:
                            for categorical in categoricals:
                                value = data[data_mapping[categorical]]
                                the_name = f"{file_name}-{categorical}/{value}"
                                row_names.append(the_name)
                                self.name_labels[the_name] = value
                                if the_name not in self.names:
                                    self.names.append(the_name)
                        else:
                            row_names.append(file_name)
                        summary_file_names.extend(row_names)
                        # create the summary
                        summary = FunctionRunSummary(fn_input_info, metrics_list, features_list)
                        # append to summaries
                        summaries.append(summary)
                        # This row's names only. Reading the whole accumulated
                        # list would give every name every function_name and
                        # make the pass quadratic in row count.
                        for name in row_names:
                            if name not in self.function_names:
                                self.function_names[name] = set()
                            self.function_names[name].add(function_name)
                    
                    # add the summaries to the appropriate place
                    for i in range(len(summaries)):
                        if summary_file_names[i] not in self.summaries:
                            self.summaries[summary_file_names[i]] = []
                        self.summaries[summary_file_names[i]].append(summaries[i])
                    
                    self.features = input_feature_names
            except FileNotFoundError:
                print(f"File '{file_name}' not found.")
                exit(1)
        self.storage = InfoStorage(metrics, input_feature_names, self.names, input_dir)
        print(f"self.storage {self.storage}")
        self.storage.build_storage(self)
        print("function name in read csvs func: ",self.function_names)

    ###
    #
    # Plotting Methods
    #
    ###

    def _label(self, name):
        """A legend label for a name.

        `self.names` holds absolute CSV paths because they key the storage, and
        printing one into a legend covers the plot. When `read_csvs` split the
        file on a categorical, the label is that categorical's value, so each
        system reads as its own name rather than as a copy of the subject
        name. Otherwise the subject directory the file sits in identifies it
        ("json" for output/json/summary.csv).
        """
        if name in self.name_labels:
            return self.name_labels[name]
        p = os.path.normpath(str(name))
        return (os.path.basename(os.path.dirname(p))
                or os.path.splitext(os.path.basename(p))[0])

    @staticmethod
    def _slug(label):
        """`label` as a filename fragment."""
        return re.sub(r"[^0-9A-Za-z._-]+", "_", str(label)).strip("_")

    # Create a scatterplot of the metric vs. the feature for each function/summary.
    def plot_metric_vs_feature(self, metric, feature, remove_outliers = False,output_dir=None):
        os.makedirs(output_dir, exist_ok=True)
        for name in self.names:
            print(f"Plotting '{metric}' vs '{feature}' for '{name}':")
            s = self.storage.get_metric_ordered_by_feature(name, metric, feature, remove_outliers)
            x_s = [x[1] for x in s]
            y_s = [x[0] for x in s]
            plt.figure()
            label = self._label(name)
            plt.scatter(x_s, y_s, label=label)
            plt.xlabel(feature)
            plt.ylabel(metric)
            if autoscale_y(y_s):
                plt.title(f"'{metric}' vs '{feature}' [log scale]")
            plt.legend()
            # The label is in the filename because this loop writes one file per
            # name. With the summary split per system, a shared filename would
            # have the systems overwrite each other and only the last survive.
            filename=f"{metric}_vs_{feature}_{self._slug(label)}.png".replace(" ", "_")
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath)
            print(f"Saved plot to {filepath}")
            plt.close()
            #plt.show()

    # 
    
    def fit_model_for_metric_and_feature(self, metric, feature, remove_outliers = False,output_dir=None):
        os.makedirs(output_dir, exist_ok=True)
        for name in self.names:
            data = self.storage.get_metric_ordered_by_feature(name, metric, feature, remove_outliers)
            
            feature_vals = [x[1] for x in data]
            metric_vals = [x[0] for x in data]

            # Drop the rows a fit cannot use, rather than abandoning the fit.
            # A censored measurement arrives as NaN and a zero feature cannot be
            # fitted, and neither should discard every other row with it: one
            # censored measurement would remove the whole plot for that metric.
            keep = [i for i in range(len(metric_vals))
                    if not math.isnan(metric_vals[i])
                    and not math.isnan(feature_vals[i])
                    and metric_vals[i] > 0
                    and feature_vals[i] != 0]
            dropped = len(metric_vals) - len(keep)
            if dropped:
                print(f"For '{name}', feature '{feature}' and metric '{metric}': "
                      f"dropped {dropped} of {len(metric_vals)} rows "
                      f"(censored, non-positive metric, or zero feature).")
            metric_vals = [metric_vals[i] for i in keep]
            feature_vals = [feature_vals[i] for i in keep]
            if len(metric_vals) < 3:
                print(f"For '{name}', feature '{feature}' and metric '{metric}': "
                      f"only {len(metric_vals)} usable rows; skipping fit.")
                continue
            try:
                # Scale-free fit and comparison. big_o's own inference
                # minimises unweighted absolute error, so on a metric spanning
                # decades the top few points choose the class; see
                # core/model_fit.py.
                best, others = model_fit.infer_complexity(feature_vals, metric_vals)
                print(f"For '{name}', feature '{feature}' and metric '{metric}' the best fit is:")
                print(big_o.reports.big_o_report(best, others))
                # A selection the data did not make on its own. These are the
                # candidates a targeted request should be asked to separate.
                tied = model_fit.near_ties(others)
                if len(tied) > 1:
                    names = ", ".join(type(t).__name__ for t in tied)
                    print(f"   [near-tie] within {model_fit.SIMPLICITY_BIAS:.0%}: "
                          f"{names} -- chosen by the simplicity bias, not the data.")
                exp = model_fit.fitted_exponent(feature_vals, metric_vals)
                if exp is not None:
                    print(f"   [exponent] free-exponent fit: {metric} ~ {feature} ** {exp:.2f}")

                # ... and plot it
                label = self._label(name)
                plt.figure()
                plt.scatter(feature_vals, metric_vals, label=label)
                log_y = autoscale_y(metric_vals)
                # Draw the fit in x order: plotting it in corpus order joins the
                # points back and forth and renders the curve as a zigzag.
                xs = sorted(feature_vals)
                ys = list(best.compute(np.asanyarray(xs)))
                if log_y:
                    # A fit can go non-positive inside the observed range (a
                    # quadratic with a negative intercept does), which a log
                    # axis cannot draw: it renders as a spike off the bottom.
                    kept = [(x, y) for x, y in zip(xs, ys) if y > 0]
                    xs = [x for x, _ in kept]
                    ys = [y for _, y in kept]
                if xs:
                    plt.plot(xs, ys, label=f"{label} fit")
                plt.title(f"'{metric}' vs '{feature}', incl. lines of best fit"
                          + (" [log scale]" if log_y else ""))
                plt.xlabel(feature)
                plt.ylabel(metric)
                plt.legend()
                filename=f"fitmodel_{metric}_vs_{feature}_{self._slug(label)}.png".replace(" ", "_")
                filepath = os.path.join(output_dir, filename)
                plt.savefig(filepath)
                print(f"Saved fit model plot to {filepath}")
                plt.close()
                #plt.show()
            except Exception as e:
                print(f"[ERROR] Could not fit model for '{name}': {e}")
                continue
        
    # subset is a list of indices to focus on, if any
    def fit_model_for_metric_and_features(self, metric, features, interaction = False, remove_outliers = False,output_dir=None):
        os.makedirs(output_dir, exist_ok=True)
        complexity_classes = [
            "Linear",
            "Quadratic",
            "Cubic",
            "Logarithmic",
            "Exponential",
            "LogLinear"
            # There's more, but these are probably the most common
            # "Constant"
            # "Polynomial"
        ]  

        def build_fun_for_complexity_class(complexity_class):
            if complexity_class == "Linear":
                return lambda x: x
            elif complexity_class == "Quadratic":
                return lambda x: x ** 2
            elif complexity_class == "Cubic":
                return lambda x: x ** 3
            elif complexity_class == "Logarithmic":
                return lambda x: math.log(x)
            elif complexity_class == "Exponential":
                return lambda x: math.exp(x)
            elif complexity_class == "LogLinear":
                return lambda x: x * math.log(x)
            else:
                return lambda x: x

        def build_complete_fun_for_complexity_classes(complexity_classes, coefficients):
            # The complexity classes is a tuple of three complexity classes.
            constant = coefficients[0]
            fn_ft1 = build_fun_for_complexity_class(complexity_classes[0])
            fn_ft2 = build_fun_for_complexity_class(complexity_classes[1])
            # fn_int = build_fun_for_complexity_class(complexity_classes[2])

            return lambda x, y : constant + coefficients[1]*fn_ft1(x) + coefficients[2]*fn_ft2(y) 
        #+ coefficients[3]*fn_ft1(x)*fn_ft2(y)

        def transform_feature_vals(feature_vals, complexity_class):
            fn_for_class = build_fun_for_complexity_class(complexity_class)
            return np.array([fn_for_class(x) for x in feature_vals])

        # If there are interaction terms...
        interaction_terms = []
        if interaction:
            for i in range(len(features)):
                for j in range(i + 1, len(features)):
                    interaction_terms.append((features[i], features[j]))

        model_fit_results = dict()
        # Idea: we are going to try the various complexity classes _for each feature_.
        # We will then compare the R^2 values and the coefficients.
        for name in self.names:
            model_fit_results[name] = dict()
            # Make all combinations of complexity classes of each feature.
            # There will be |complexity_classes|^|features| combinations.
            # They shall be tuples (complexity_class, ..., complexity_class) 
            # and the length of the tuple will be the number of features.
            # We will then fit the model for each combination.
            # 
            # (1) Make |complexity_classes|^|features| combinations.
            complexity_combos = []
            for i in range(len(complexity_classes) ** (len(features) + len(interaction_terms))):
                # This is total witchcraft.
                complexity_combos.append(tuple([complexity_classes[i // (len(complexity_classes) ** j) % len(complexity_classes)] for j in range(len(features) + len(interaction_terms))]))

            for combo in complexity_combos:
                model_fit_results[name][combo] = dict()

        best_complexity_combos = dict()

        # extract the data and model
        for name in self.names:
            # This is going to run once per name, i.e., once per summary file.
            # We should extract the data for the metric and the features.
            metric_vals = self.storage.get_metric(name, metric)
            feature_vals = []
            for feature in features:
                these_features = self.storage.get_feature(name, feature)
                feature_vals.append(these_features)
            #to avoid crashing if metrics and features are None
            if len(metric_vals) == 0 or any(len(f) == 0 for f in feature_vals):
                print(f"[WARNING] Skipping '{name}' — empty metric or feature values.")
                continue

            if remove_outliers:
                z_scores = ss.zscore(metric_vals)

            # Sanitize the data.
            indices_to_remove = []
            for i in range(len(metric_vals)):
                metric_nan = math.isnan(metric_vals[i])
                features_nan = any([math.isnan(x[i]) for x in feature_vals])
                metric_zero = metric_vals[i] == 0
                features_zero = any([x[i] == 0 for x in feature_vals])
                metric_neg = metric_vals[i] < 0
                features_neg = any([x[i] < 0 for x in feature_vals])
                if remove_outliers and abs(z_scores[i]) > 3:
                    indices_to_remove.append(i)
                elif metric_nan or features_nan or metric_zero or features_zero or metric_neg or features_neg:
                    indices_to_remove.append(i)

            # Remove the indices.
            metric_vals = [metric_vals[i] for i in range(len(metric_vals)) if i not in indices_to_remove]
            for i in range(len(feature_vals)):
                feature_vals[i] = [x for j, x in enumerate(feature_vals[i]) if j not in indices_to_remove]

            # The sanitizer drops a row when ANY feature on it is zero, so a
            # joint fit over several features that each reach zero can discard
            # every row, since few inputs carry every counted construct at
            # once. The same emptiness check runs before
            # sanitizing; without it here, add_constant reduces over a
            # zero-size array and takes the whole run down after the loop has
            # already paid for its measurements.
            if not metric_vals:
                print(f"[WARNING] Skipping joint fit for '{name}' on "
                      f"{features}: all {len(indices_to_remove)} rows dropped "
                      f"(a feature is zero on every row). The single-feature "
                      f"fits still cover these properties.")
                continue

            # We're trying to use statsmodels OLS, so the feature_vals array should be transposed.
            feature_vals = np.array(feature_vals).T

            # Assume independence of the feature vals, and other assumptions.

            # For each combination of complexity classes, fit the model.
            this_model_fit_results = model_fit_results[name]
            complexity_combos = list(this_model_fit_results.keys())
            for combo in complexity_combos:
                # Based on the complexity class combination, we need to 
                # transform the feature_vals.
                # Make a copy of the feature_vals.
                feature_vals_this_combo = np.copy(feature_vals)
                try:
                    for i in range(len(features)):
                        the_combo = combo[i]
                        feature_vals_this_combo[:, i] = transform_feature_vals(feature_vals_this_combo[:, i], the_combo)
                except OverflowError:
                    print(f"Overflow error for '{name}' and combo '{combo}'.")
                    this_model_fit_results[combo] = (-1, None)
                    continue

                # If there are interaction terms, we will compute them here.
                for interaction_term in interaction_terms:
                    feature_1 = features.index(interaction_term[0])
                    feature_2 = features.index(interaction_term[1])
                    interaction_vals = feature_vals_this_combo[:, feature_1] * feature_vals_this_combo[:, feature_2]
                    feature_vals_this_combo = np.column_stack((feature_vals_this_combo, interaction_vals))

                # Let's fit the model.
                # They suggest adding a constant to the feature_vals.
                # has_constant="add" forces an intercept even when a feature
                # column is constant (degenerate data); otherwise add_constant
                # silently skips it and the coefficient vector comes back one
                # short, breaking the AUC/fitted-value math below.
                feature_vals_this_combo = sm.add_constant(feature_vals_this_combo, has_constant="add")
                # Weighted for the same reason the single-feature fit is: OLS
                # here compares combinations on an R^2 that the largest metric
                # values dominate. WLS with 1/y^2 makes the criterion relative,
                # and its rsquared is computed on the weighted data.
                model = sm.WLS(metric_vals, feature_vals_this_combo,
                               weights=model_fit.relative_weights(metric_vals)).fit()
                
                # Collect R^2 and coefficients.
                r_squared = model.rsquared
                coefficients = model.params

                this_model_fit_results[combo] = (r_squared, coefficients)

            # can't reload b/c we removed some stuff above.
            # metric_vals = self.storage.get_metric(name, metric)
            print(f"Model fit results for '{name}':")
            best_r_squared = -1
            best_combo = None
            best_coeffs = None
            for combo in complexity_combos:
                r_squared, coefficients = model_fit_results[name][combo]
                #to avoid crashing the function if there are no coefficients
                if coefficients is None:
                    continue
                if r_squared > best_r_squared:
                    best_r_squared = r_squared
                    best_combo = combo
                    best_coeffs = coefficients
            #to avoid crashing the function if there are no best_coeffs
            if best_coeffs is None:
                print(f"[WARNING] Could not find a valid model fit for '{name}'.Skipping.")
                continue

            print(f"Best fit for '{name}':")
            print(f"R^2: {best_r_squared}")
            print(f"Intercept: {best_coeffs[0]}")
            for i in range(len(features)):
                #wrap with if and else
                if (i+1) < len(best_coeffs):
                    print(f"Feature '{features[i]}' has complexity class '{best_combo[i]}'.")
                    print(f"The coefficient for this feature is {best_coeffs[i + 1]}.")
                else:
                    print(f"[WARNING] Missing coefficient for feature '{features[i]}'. Only {len(best_coeffs)} coefficients found.")
            if interaction:
                for i in range(len(interaction_terms)):
                    print(f"Interaction term '{interaction_terms[i][0]} * {interaction_terms[i][1]}' has complexity class '{best_combo[len(features) + i]}'.")
                    print(f"The coefficient for this interaction term is {best_coeffs[len(features) + i + 1]}")

            best_complexity_combos[name] = best_combo

            # Build the fitted function for the best fit.
            # Assume two features and interaction.
            fn_for_model = build_complete_fun_for_complexity_classes(best_combo, best_coeffs)

            # We will plot the best fit.
            # z : metric value and also the predicted metric value
            # x : feature 1
            # y : feature 2

            # Compute best fit.
            fitted_metric_vals = []
            constant = best_coeffs[0]
            feature_values_1 = feature_vals[:, 0]
            feature_values_2 = feature_vals[:, 1]
            transformed_feature_values_1 = transform_feature_vals(feature_values_1, best_combo[0])
            transformed_feature_values_2 = transform_feature_vals(feature_values_2, best_combo[1])
            for i in range(len(metric_vals)):
                fitted_metric_vals.append(constant + best_coeffs[1] * transformed_feature_values_1[i] + best_coeffs[2] * transformed_feature_values_2[i])

            if interaction:
                # Assuming again only two features.
                interaction_vals = transformed_feature_values_1 * transformed_feature_values_2
                for i in range(len(metric_vals)):
                    # Also not right, depends on the complexity class of the interaction term.
                    fitted_metric_vals[i] += best_coeffs[3] * interaction_vals[i]

            fig = plt.figure()
            ax = fig.add_subplot(111, projection='3d')
            ax.scatter(feature_values_1, feature_values_2, metric_vals, label = "actual")
            ax.scatter(feature_values_1, feature_values_2, fitted_metric_vals, label = "fitted")
            # can we get the fitted values as ameshgrid?
            # X, Y = np.meshgrid(feature_values_1, feature_values_2)
            # Z = # ???
            # ax.plot_surface(X, Y, Z, alpha = 0.5)
            ax.set_xlabel(features[0])
            ax.set_ylabel(features[1])
            ax.set_zlabel(metric)
            # title
            ax.set_title(f"Best fit for '{name}'")
            # dump it
            # only_basename_no_ext = os.path.splitext(name)[0]
            # pickle.dump(ax, open(f"{only_basename_no_ext}_{metric}_{features[0]}_{features[1]}_3d_model.p", "wb"))
            plt.legend()
            # The filename names every feature of the joint fit, so the plot
            # does not claim to be about one of them.
            joint = "_and_".join(features)
            filename=f"3dmodel_{metric}_vs_{joint}_{self._slug(self._label(name))}.png".replace(" ", "_")
            filepath = os.path.join(output_dir, filename)
            plt.savefig(filepath)
            print(f"Saved 3d fit model plot to {filepath}")
            plt.close()
            #plt.show()

        # No area-under-curve verdict is computed from the fitted surface.
        # Integrating it needs limits that suit every subject's properties,
        # and it names a single global winner, which `core.compare`'s regional
        # dominance can contradict. The overall comparison is
        # `compare.weighted_ratio`, which reweights the measured ratios so
        # each region counts once instead of integrating a fit, and states
        # its measure.
        for name in self.names:
            if name in best_complexity_combos:
                print(f"Best complexity classes for '{name}': "
                      f"{best_complexity_combos[name]}")
        print("======================================================================")
    
    ###
    #
    # End Plotting Methods
    #
    ###
