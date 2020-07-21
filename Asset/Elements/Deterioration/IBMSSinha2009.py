import numpy as np

from .BaseDeteriorationModel import *

class Markovian(BaseDeteriorationModel):

	def __init__(self):
		super().__init__()
		"""
		This is based on IBMS by Sinha et. al. 2009
		To be completed
		"""

	def predict_condition(self, previous_condition, age = None):

		if self.element.name == SUPERSTRUCTURE:
			if self.asset.road_class == NHS or self.asset.road_class == MAJOR:
				if self.element.asset.material == STEEL or self.element.asset.material == TIMBER:
					
					if self.element.age in range(0, 7): probs_list = [0.976, 0.936, 0.890, 0.885, 0.920, 0.930, 0.920, 1.0]
					elif self.element.age in range (7, 13): probs_list = [0.951, 0.930, 0.903, 0.900, 0.910, 0.915, 0.910, 1.0]
					elif self.element.age in range (13, 19): probs_list = [0.948, 0.930, 0.855, 0.870, 0.880, 0.870, 0.860, 1.0]
					elif self.element.age in range (19, 25): probs_list = [0.945, 0.920, 0.830, 0.850, 0.868, 0.870, 0.865, 1.0]
					elif self.element.age in range (25, 31): probs_list = [0.940, 0.918, 0.857, 0.852, 0.870, 0.880, 0.870, 1.0]
					elif self.element.age in range (31, 37): probs_list = [0.930, 0.912, 0.847, 0.865, 0.874, 0.870, 0.870, 1.0]
					elif self.element.age in range (37, 43): probs_list = [0.955, 0.957, 0.905, 0.908, 0.907, 0.892, 0.860, 1.0]
					elif self.element.age in range (43, 49): probs_list = [0.950, 0.945, 0.925, 0.933, 0.925, 0.918, 0.850, 1.0]
					elif self.element.age in range (49, 55): probs_list = [0.945, 0.956, 0.930, 0.945, 0.945, 0.912, 0.876, 1.0]
					elif self.element.age in range (55, 61): probs_list = [0.943, 0.955, 0.928, 0.948, 0.955, 0.920, 0.886, 1.0]
					elif self.element.age in range (61, 67): probs_list = [0.940, 0.955, 0.932, 0.960, 0.955, 0.925, 0.886, 1.0]
					elif self.element.age in range (67, 73): probs_list = [0.890, 0.912, 0.948, 0.958, 0.959, 0.938, 0.910, 1.0]
					elif self.element.age in range (73, 79): probs_list = [0.870, 0.890, 0.943, 0.957, 0.957, 0.948, 0.928, 1.0]
					elif self.element.age in range (79, 85): probs_list = [0.870, 0.905, 0.941, 0.957, 0.953, 0.955, 0.925, 1.0]
					elif self.element.age in range (85, 91): probs_list = [0.850, 0.850, 0.937, 0.956, 0.954, 0.950, 0.930, 1.0]
					else: probs_list = [0.850, 0.850, 0.937, 0.956, 0.954, 0.950, 0.930, 1.0]

				else:

					if self.element.age in range(0, 7): probs_list = [0.989, 0.97, 0.937, 0.955, 0.92, 0.9, 0.9, 1.0]
					elif self.element.age in range (7, 13): probs_list = [0.962, 0.958, 0.925, 0.92, 0.89, 0.88, 0.87, 1.0]
					elif self.element.age in range (13, 19): probs_list = [0.966, 0.945, 0.88, 0.88, 0.89, 0.88, 0.87, 1.0]
					elif self.element.age in range (19, 25): probs_list = [0.95, 0.93, 0.87, 0.88, 0.87, 0.88, 0.87, 1.0]
					elif self.element.age in range (25, 31): probs_list = [0.95, 0.932, 0.872, 0.88, 0.87, 0.88, 0.87, 1.0]
					elif self.element.age in range (31, 37): probs_list = [0.952, 0.935, 0.878, 0.888, 0.878, 0.88, 0.87, 1.0]
					elif self.element.age in range (37, 43): probs_list = [0.95, 0.93, 0.865, 0.88, 0.868, 0.87, 0.85, 1.0]
					elif self.element.age in range (43, 49): probs_list = [0.94, 0.92, 0.855, 0.875, 0.86, 0.866, 0.85, 1.0]
					elif self.element.age in range (49, 55): probs_list = [0.94, 0.95, 0.885, 0.915, 0.92, 0.9, 0.876, 1.0]
					elif self.element.age in range (55, 61): probs_list = [0.93, 0.95, 0.898, 0.92, 0.93, 0.91, 0.876, 1.0]
					elif self.element.age in range (61, 67): probs_list = [0.92, 0.955, 0.912, 0.936, 0.955, 0.923, 0.886, 1.0]
					elif self.element.age in range (67, 73): probs_list = [0.89, 0.912, 0.958, 0.968, 0.969, 0.948, 0.92, 1.0]
					elif self.element.age in range (73, 79): probs_list = [0.87, 0.87, 0.933, 0.94, 0.937, 0.938, 0.928, 1.0]
					elif self.element.age in range (79, 85): probs_list = [0.86, 0.865, 0.931, 0.953, 0.946, 0.945, 0.918, 1.0]
					elif self.element.age in range (85, 91): probs_list = [0.85, 0.85, 0.937, 0.96, 0.954, 0.95, 0.93, 1.0]
					else: probs_list = [0.85, 0.85, 0.937, 0.96, 0.954, 0.95, 0.93, 1.0]

			elif self.asset.road_class == MINOR or self.asset.road_class == LOCAL:
				if self.element.asset.material == STEEL or self.element.asset.material == TIMBER:
					if self.element.age in range(0, 7): probs_list = [0.987, 0.974, 0.95, 0.955, 0.92, 0.9, 0.9, 1.0]
					elif self.element.age in range (7, 13): probs_list = [0.972, 0.945, 0.935, 0.91, 0.91, 0.88, 0.88, 1.0]
					elif self.element.age in range (13, 19): probs_list = [0.952, 0.934, 0.865, 0.865, 0.87, 0.86, 0.83, 1.0]
					elif self.element.age in range (19, 25): probs_list = [0.943, 0.925, 0.905, 0.915, 0.915, 0.93, 0.92, 1.0]
					elif self.element.age in range (25, 31): probs_list = [0.938, 0.89, 0.905, 0.88, 0.865, 0.928, 0.9, 1.0]
					elif self.element.age in range (31, 37): probs_list = [0.924, 0.885, 0.912, 0.907, 0.904, 0.898, 0.89, 1.0]
					elif self.element.age in range (37, 43): probs_list = [0.925, 0.912, 0.911, 0.913, 0.932, 0.941, 0.931, 1.0]
					elif self.element.age in range (43, 49): probs_list = [0.941, 0.937, 0.937, 0.938, 0.945, 0.938, 0.928, 1.0]
					elif self.element.age in range (49, 55): probs_list = [0.925, 0.941, 0.945, 0.94, 0.95, 0.935, 0.92, 1.0]
					elif self.element.age in range (55, 61): probs_list = [0.89, 0.917, 0.963, 0.965, 0.975, 0.957, 0.923, 1.0]
					elif self.element.age in range (61, 67): probs_list = [0.9, 0.912, 0.962, 0.963, 0.972, 0.962, 0.913, 1.0]
					elif self.element.age in range (67, 73): probs_list = [0.885, 0.912, 0.957, 0.965, 0.965, 0.955, 0.91, 1.0]
					elif self.element.age in range (73, 79): probs_list = [0.875, 0.911, 0.958, 0.966, 0.975, 0.965, 0.932, 1.0]
					elif self.element.age in range (79, 85): probs_list = [0.87, 0.9, 0.952, 0.965, 0.969, 0.965, 0.92, 1.0]
					elif self.element.age in range (85, 91): probs_list = [0.85, 0.881, 0.95, 0.965, 0.967, 0.965, 0.93, 1.0]
					else: probs_list = [0.85, 0.881, 0.95, 0.965, 0.967, 0.965, 0.93, 1.0]

				else:
					if self.element.age in range(0, 7): probs_list = [0.989, 0.979, 0.96, 0.965, 0.95, 0.92, 0.91, 1.0]
					elif self.element.age in range (7, 13): probs_list = [0.986, 0.969, 0.95, 0.94, 0.92, 0.9, 0.89, 1.0]
					elif self.element.age in range (13, 19): probs_list = [0.962, 0.942, 0.875, 0.875, 0.88, 0.87, 0.84, 1.0]
					elif self.element.age in range (19, 25): probs_list = [0.957, 0.945, 0.933, 0.925, 0.925, 0.94, 0.92, 1.0]
					elif self.element.age in range (25, 31): probs_list = [0.954, 0.922, 0.93, 0.905, 0.894, 0.938, 0.9, 1.0]
					elif self.element.age in range (31, 37): probs_list = [0.944, 0.92, 0.925, 0.92, 0.91, 0.908, 0.89, 1.0]
					elif self.element.age in range (37, 43): probs_list = [0.935, 0.912, 0.915, 0.919, 0.928, 0.936, 0.92, 1.0]
					elif self.element.age in range (43, 49): probs_list = [0.938, 0.897, 0.913, 0.91, 0.904, 0.91, 0.88, 1.0]
					elif self.element.age in range (49, 55): probs_list = [0.925, 0.933, 0.94, 0.931, 0.928, 0.9, 0.875, 1.0]
					elif self.element.age in range (55, 61): probs_list = [0.89, 0.88, 0.941, 0.933, 0.956, 0.935, 0.9, 1.0]
					elif self.element.age in range (61, 67): probs_list = [0.9, 0.907, 0.96, 0.963, 0.963, 0.945, 0.9, 1.0]
					elif self.element.age in range (67, 73): probs_list = [0.88, 0.91, 0.952, 0.958, 0.961, 0.941, 0.91, 1.0]
					elif self.element.age in range (73, 79): probs_list = [0.875, 0.894, 0.954, 0.962, 0.967, 0.958, 0.932, 1.0]
					elif self.element.age in range (79, 85): probs_list = [0.87, 0.89, 0.947, 0.96, 0.966, 0.956, 0.92, 1.0]
					elif self.element.age in range (85, 91): probs_list = [0.85, 0.881, 0.957, 0.97, 0.968, 0.965, 0.94, 1.0]
					else: probs_list = [0.85, 0.881, 0.957, 0.97, 0.968, 0.965, 0.94, 1.0]


		elif self.element.name == SUBSTRUCTURE:
			if self.element.age in range(0, 7): probs_list = [0.9955, 0.993, 0.989, 0.987, 0.985, 0.98, 0.98, 1.0]
			elif self.element.age in range (7, 13): probs_list = [0.976, 0.971, 0.976, 0.983, 0.985, 0.97, 0.97, 1.0]
			elif self.element.age in range (13, 19): probs_list = [0.972, 0.935, 0.944, 0.95, 0.935, 0.93, 0.93, 1.0]
			elif self.element.age in range (19, 25): probs_list = [0.954, 0.92, 0.923, 0.943, 0.955, 0.94, 0.92, 1.0]
			elif self.element.age in range (25, 31): probs_list = [0.954, 0.922, 0.93, 0.925, 0.934, 0.938, 0.9, 1.0]
			elif self.element.age in range (31, 37): probs_list = [0.944, 0.92, 0.925, 0.922, 0.924, 0.928, 0.89, 1.0]
			elif self.element.age in range (37, 43): probs_list = [0.939, 0.915, 0.918, 0.917, 0.919, 0.92, 0.89, 1.0]
			elif self.element.age in range (43, 49): probs_list = [0.929, 0.895, 0.905, 0.907, 0.9, 0.91, 0.88, 1.0]
			elif self.element.age in range (49, 55): probs_list = [0.929, 0.936, 0.945, 0.935, 0.935, 0.91, 0.88, 1.0]
			elif self.element.age in range (55, 61): probs_list = [0.89, 0.88, 0.94, 0.935, 0.955, 0.91, 0.88, 1.0]
			elif self.element.age in range (61, 67): probs_list = [0.9, 0.907, 0.958, 0.96, 0.96, 0.94, 0.9, 1.0]
			elif self.element.age in range (67, 73): probs_list = [0.89, 0.912, 0.958, 0.965, 0.966, 0.948, 0.92, 1.0]
			elif self.element.age in range (73, 79): probs_list = [0.87, 0.89, 0.95, 0.96, 0.964, 0.955, 0.928, 1.0]
			elif self.element.age in range (79, 85): probs_list = [0.87, 0.891, 0.951, 0.963, 0.966, 0.955, 0.928, 1.0]
			elif self.element.age in range (85, 91): probs_list = [0.85, 0.88, 0.955, 0.968, 0.968, 0.965, 0.94, 1.0]
			else: probs_list = [0.85, 0.88, 0.955, 0.968, 0.968, 0.965, 0.94, 1.0]

		elif self.element.name == DECK:
			if self.asset.road_class == NHS:
				if self.element.age in range(0, 7): probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
				elif self.element.age in range (7, 13): probs_list = [0.59, 0.555, 0.64, 0.68, 0.71, 0.67, 0.55, 1.0]
				elif self.element.age in range (13, 19): probs_list = [0.63, 0.67, 0.66, 0.64, 0.684, 0.68, 0.66, 1.0]
				elif self.element.age in range (19, 25): probs_list = [0.65, 0.78, 0.84, 0.838, 0.768, 0.745, 0.68, 1.0]
				elif self.element.age in range (25, 31): probs_list = [0.77, 0.83, 0.96, 0.95, 0.95, 0.96, 0.85, 1.0]
				else: probs_list = [0.77, 0.83, 0.96, 0.95, 0.95, 0.96, 0.85, 1.0]

			elif self.asset.road_class == MAJOR:
				if self.element.age in range(0, 7): probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
				elif self.element.age in range (7, 13): probs_list = [0.59, 0.555, 0.64, 0.68, 0.71, 0.67, 0.55, 1.0]
				elif self.element.age in range (13, 19): probs_list = [0.63, 0.67, 0.66, 0.64, 0.684, 0.68, 0.66, 1.0]
				elif self.element.age in range (19, 25): probs_list = [0.65, 0.78, 0.84, 0.838, 0.768, 0.745, 0.68, 1.0]
				elif self.element.age in range (25, 31): probs_list = [0.77, 0.83, 0.96, 0.95, 0.95, 0.96, 0.85, 1.0]
				else: probs_list = [0.77, 0.83, 0.96, 0.95, 0.95, 0.96, 0.85, 1.0]

			elif self.asset.road_class == MINOR:
				if self.element.age in range(0, 7): probs_list = [0.978, 0.971, 0.858, 0.8, 0.75, 0.7, 0.6, 1.0]
				elif self.element.age in range (7, 13): probs_list = [0.71, 0.68, 0.68, 0.645, 0.68, 0.67, 0.55, 1.0]
				elif self.element.age in range (13, 19): probs_list = [0.78, 0.755, 0.64, 0.64, 0.63, 0.63, 0.66, 1.0]
				elif self.element.age in range (19, 25): probs_list = [0.65, 0.78, 0.7, 0.75, 0.725, 0.78, 0.75, 1.0]
				elif self.element.age in range (25, 31): probs_list = [0.77, 0.83, 0.9, 0.92, 0.96, 0.96, 0.83, 1.0]
				else: probs_list = [0.77, 0.83, 0.9, 0.92, 0.96, 0.96, 0.83, 1.0]

			elif self.asset.road_class == LOCAL:
				if self.element.age in range(0, 7): probs_list = [0.988, 0.971, 0.878, 0.8, 0.75, 0.77, 0.6, 1.0]
				elif self.element.age in range (7, 13): probs_list = [0.864, 0.85, 0.725, 0.745, 0.71, 0.67, 0.55, 1.0]
				elif self.element.age in range (13, 19): probs_list = [0.82, 0.82, 0.68, 0.72, 0.684, 0.68, 0.66, 1.0]
				elif self.element.age in range (19, 25): probs_list = [0.65, 0.78, 0.8, 0.75, 0.645, 0.65, 0.68, 1.0]
				elif self.element.age in range (25, 31): probs_list = [0.77, 0.83, 0.86, 0.86, 0.89, 0.9, 0.75, 1.0]
				else: probs_list = [0.77, 0.83, 0.86, 0.86, 0.89, 0.9, 0.75, 1.0]

		elif self.element.name == ARCH:
			if self.element.age in range(0, 7): probs_list = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
			elif self.element.age in range (7, 13): probs_list = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
			elif self.element.age in range (13, 19): probs_list = [0.9955, 0.99, 0.98, 0.977, 0.965, 0.96, 0.96, 1.0]
			elif self.element.age in range (19, 25): probs_list = [0.982, 0.935, 0.959, 0.96, 0.94, 0.938, 0.945, 1.0]
			elif self.element.age in range (25, 31): probs_list = [0.96, 0.932, 0.935, 0.94, 0.93, 0.925, 0.922, 1.0]
			elif self.element.age in range (31, 37): probs_list = [0.966, 0.935, 0.93, 0.946, 0.955, 0.94, 0.92, 1.0]
			elif self.element.age in range (37, 43): probs_list = [0.952, 0.921, 0.926, 0.92, 0.93, 0.933, 0.895, 1.0]
			elif self.element.age in range (43, 49): probs_list = [0.94, 0.918, 0.92, 0.917, 0.92, 0.92, 0.884, 1.0]
			elif self.element.age in range (49, 55): probs_list = [0.94, 0.917, 0.915, 0.915, 0.919, 0.92, 0.89, 1.0]
			elif self.element.age in range (55, 61): probs_list = [0.927, 0.893, 0.907, 0.913, 0.918, 0.93, 0.9, 1.0]
			elif self.element.age in range (61, 67): probs_list = [0.92, 0.915, 0.91, 0.905, 0.91, 0.885, 0.84, 1.0]
			elif self.element.age in range (67, 73): probs_list = [0.88, 0.87, 0.939, 0.938, 0.96, 0.911, 0.87, 1.0]
			elif self.element.age in range (73, 79): probs_list = [0.898, 0.905, 0.957, 0.955, 0.953, 0.935, 0.89, 1.0]
			elif self.element.age in range (79, 85): probs_list = [0.89, 0.91, 0.955, 0.962, 0.963, 0.945, 0.91, 1.0]
			elif self.element.age in range (85, 91): probs_list = [0.875, 0.895, 0.953, 0.96, 0.97, 0.963, 0.94, 1.0]
			elif self.element.age in range (91, 97): probs_list = [0.877, 0.896, 0.958, 0.967, 0.969, 0.965, 0.945, 1.0]
			elif self.element.age in range (97, 103): probs_list = [0.85, 0.88, 0.955, 0.965, 0.965, 0.97, 0.948, 1.0]
			elif self.element.age in range (103, 109): probs_list = [0.855, 0.892, 0.965, 0.972, 0.982, 0.983, 0.965, 1.0]
			elif self.element.age in range (107, 115): probs_list = [0.858, 0.888, 0.963, 0.973, 0.972, 0.973, 0.96, 1.0]
			elif self.element.age in range (113, 121): probs_list = [0.855, 0.886, 0.96, 0.973, 0.972, 0.972, 0.955, 1.0]
			else: probs_list = [0.855, 0.886, 0.96, 0.973, 0.972, 0.972, 0.955, 1.0]

		elif self.element.name == WEARING:
			if self.asset.road_class == NHS: 
				if self.element.age in range(0, 7): probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
				elif self.element.age in range (7, 13): probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
				elif self.element.age in range (13, 19): probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
				elif self.element.age in range (19, 25): probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
				elif self.element.age in range (25, 31): probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
				else: probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]

			elif self.asset.road_class == MAJOR:
				if self.element.age in range(0, 7): probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
				elif self.element.age in range (7, 13): probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
				elif self.element.age in range (13, 19): probs_list = [0.63, 0.67, 0.66, 0.64, 0.684, 0.68, 0.66, 1.0]
				elif self.element.age in range (19, 25): probs_list = [0.65, 0.78, 0.84, 0.838, 0.768, 0.745, 0.68, 1.0]
				elif self.element.age in range (25, 31): probs_list = [0.77, 0.83, 0.96, 0.95, 0.95, 0.96, 0.85, 1.0]
				else: probs_list = [0.77, 0.83, 0.96, 0.95, 0.95, 0.96, 0.85, 1.0]

			elif self.asset.road_class == MINOR:
				if self.element.age in range(0, 7): probs_list = [0.978, 0.971, 0.858, 0.8, 0.75, 0.7, 0.6, 1.0]
				elif self.element.age in range (7, 13): probs_list = [0.71, 0.68, 0.68, 0.645, 0.68, 0.67, 0.55, 1.0]
				elif self.element.age in range (13, 19): probs_list = [0.78, 0.755, 0.64, 0.64, 0.63, 0.63, 0.66, 1.0]
				elif self.element.age in range (19, 25): probs_list = [0.65, 0.78, 0.7, 0.75, 0.725, 0.78, 0.75, 1.0]
				elif self.element.age in range (25, 31): probs_list = [0.77, 0.83, 0.9, 0.92, 0.96, 0.96, 0.83, 1.0]
				else: probs_list = [0.77, 0.83, 0.9, 0.92, 0.96, 0.96, 0.83, 1.0]

			elif self.asset.road_class == LOCAL:
				if self.element.age in range(0, 7): probs_list = [0.988, 0.971, 0.878, 0.8, 0.75, 0.77, 0.6, 1.0]
				elif self.element.age in range (7, 13): probs_list = [0.864, 0.85, 0.725, 0.745, 0.71, 0.67, 0.55, 1.0]
				elif self.element.age in range (13, 19): probs_list = [0.82, 0.82, 0.68, 0.72, 0.684, 0.68, 0.66, 1.0]
				elif self.element.age in range (19, 25): probs_list = [0.65, 0.78, 0.8, 0.75, 0.645, 0.65, 0.68, 1.0]
				elif self.element.age in range (25, 31): probs_list = [0.77, 0.83, 0.86, 0.86, 0.89, 0.9, 0.75, 1.0]
				else: probs_list = [0.77, 0.83, 0.86, 0.86, 0.89, 0.9, 0.75, 1.0]

		elif self.element.name == JOINT:
			if self.asset.road_class == NHS:
				if self.element.age in range(0, 7): probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
				elif self.element.age in range (7, 13): probs_list = [0.59, 0.555, 0.64, 0.68, 0.71, 0.67, 0.55, 1.0]
				elif self.element.age in range (13, 19): probs_list = [0.63, 0.67, 0.66, 0.64, 0.684, 0.68, 0.66, 1.0]
				elif self.element.age in range (19, 25): probs_list = [0.65, 0.78, 0.84, 0.838, 0.768, 0.745, 0.68, 1.0]
				else: probs_list = [0.65, 0.78, 0.84, 0.838, 0.768, 0.745, 0.68, 1.0]

			elif self.asset.road_class == MAJOR:
				if self.element.age in range(0, 7): probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
				elif self.element.age in range (7, 13): probs_list = [0.59, 0.555, 0.64, 0.68, 0.71, 0.67, 0.55, 1.0]
				elif self.element.age in range (13, 19): probs_list = [0.63, 0.67, 0.66, 0.64, 0.684, 0.68, 0.66, 1.0]
				elif self.element.age in range (19, 25): probs_list = [0.65, 0.78, 0.84, 0.838, 0.768, 0.745, 0.68, 1.0]
				else: probs_list = [0.65, 0.78, 0.84, 0.838, 0.768, 0.745, 0.68, 1.0]

			elif self.asset.road_class == MINOR:
				if self.element.age in range(0, 7): probs_list = [0.978, 0.971, 0.858, 0.8, 0.75, 0.7, 0.6, 1.0]
				elif self.element.age in range (7, 13): probs_list = [0.71, 0.68, 0.68, 0.645, 0.68, 0.67, 0.55, 1.0]
				elif self.element.age in range (13, 19): probs_list = [0.78, 0.755, 0.64, 0.64, 0.63, 0.63, 0.66, 1.0]
				elif self.element.age in range (19, 25): probs_list = [0.65, 0.78, 0.7, 0.75, 0.725, 0.78, 0.75, 1.0]
				else: probs_list = [0.65, 0.78, 0.7, 0.75, 0.725, 0.78, 0.75, 1.0]

			elif self.asset.road_class == LOCAL:
				if self.element.age in range(0, 7): probs_list = [0.988, 0.971, 0.878, 0.8, 0.75, 0.77, 0.6, 1.0]
				elif self.element.age in range (7, 13): probs_list = [0.864, 0.85, 0.725, 0.745, 0.71, 0.67, 0.55, 1.0]
				elif self.element.age in range (13, 19): probs_list = [0.82, 0.82, 0.68, 0.72, 0.684, 0.68, 0.66, 1.0]
				elif self.element.age in range (19, 25): probs_list = [0.65, 0.78, 0.8, 0.75, 0.645, 0.65, 0.68, 1.0]
				else: probs_list = [0.65, 0.78, 0.8, 0.75, 0.645, 0.65, 0.68, 1.0]

		elif self.element.name == PATCHING:
			if self.asset.road_class == NHS: probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
			elif self.asset.road_class == MAJOR: probs_list = [0.913, 0.96, 0.864, 0.82, 0.7, 0.75, 0.6, 1.0]
			elif self.asset.road_class == MINOR: probs_list = [0.978, 0.971, 0.858, 0.8, 0.75, 0.7, 0.6, 1.0]
			elif self.asset.road_class == LOCAL: probs_list = [0.988, 0.971, 0.878, 0.8, 0.75, 0.77, 0.6, 1.0]
			else: probs_list = [0.988, 0.971, 0.878, 0.8, 0.75, 0.77, 0.6, 1.0]

		if not 'probs_list' in locals():
			print ("\n\n\n\n-----------------------------------------\n")
			print (self.element.name, self.asset.road_class, self.element.age)
			print ("\n-----------------------------------------\n\n\n\n")

		if np.random.rand() > probs_list[min(previous_condition, 7)]:
			return previous_condition + 1
		else:
			return previous_condition



		